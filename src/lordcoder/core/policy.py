"""Permission checks and mutating operations."""

from __future__ import annotations

import difflib
import shlex
import subprocess
from pathlib import Path
from typing import Iterable, List

from ..models import ApplyResponse, FileChange, TestResponse


class PolicyError(RuntimeError):
    """Raised when a policy decision blocks an operation."""


class PolicyManager:
    """Manage write and shell permissions."""

    def __init__(self, project_root: Path, allow_file_write: bool, allow_shell: bool) -> None:
        self.project_root = project_root.resolve()
        self.allow_file_write = allow_file_write
        self.allow_shell = allow_shell

    def _resolve_target(self, relative_path: str) -> Path:
        target = (self.project_root / relative_path).resolve()
        try:
            target.relative_to(self.project_root)
        except ValueError as exc:
            raise PolicyError(f"Refusing to access path outside project root: {relative_path}") from exc
        return target

    def apply_changes(self, changes: Iterable[FileChange], dry_run: bool, allow_write: bool) -> ApplyResponse:
        """Apply or preview file changes."""
        materialized = list(changes)
        if not dry_run and not (self.allow_file_write or allow_write):
            raise PolicyError("File writes are disabled. Re-run with --allow-write.")

        diffs = {}
        written_files: List[str] = []
        changed_files: List[str] = []

        for change in materialized:
            target = self._resolve_target(change.path)
            original = target.read_text(encoding="utf-8") if target.exists() else ""
            diff = "".join(
                difflib.unified_diff(
                    original.splitlines(keepends=True),
                    change.content.splitlines(keepends=True),
                    fromfile=f"a/{change.path}",
                    tofile=f"b/{change.path}",
                )
            )
            diffs[change.path] = diff
            changed_files.append(change.path)
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(change.content, encoding="utf-8")
                written_files.append(change.path)

        return ApplyResponse(
            dry_run=dry_run,
            changed_files=changed_files,
            diffs=diffs,
            written_files=written_files,
        )

    def run_test_command(self, command: str, cwd: Path | None, allow_shell: bool) -> TestResponse:
        """Run a configured command via subprocess."""
        if not (self.allow_shell or allow_shell):
            raise PolicyError("Shell execution is disabled. Re-run with --allow-shell.")
        args = shlex.split(command, posix=True)
        try:
            completed = subprocess.run(
                args,
                cwd=str(cwd or self.project_root),
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            raise PolicyError(f"Failed to run command: {exc}") from exc
        return TestResponse(
            command=args,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
