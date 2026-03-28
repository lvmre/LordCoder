"""Tests for the CLI surface."""

from __future__ import annotations

import io
import json
import shutil
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from uuid import uuid4

from lordcoder.cli import main


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"cli-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def run_cli(args: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(args)
    return code, stdout.getvalue(), stderr.getvalue()


def test_version_command() -> None:
    code, stdout, _ = run_cli(["version"])
    assert code == 0
    assert stdout.strip()


def test_init_and_doctor_json() -> None:
    root = make_workspace_temp_dir()
    try:
        code, _, _ = run_cli(["init", "--path", str(root)])
        assert code == 0
        code, stdout, _ = run_cli(["doctor", "--path", str(root), "--json"])
        payload = json.loads(stdout)
        assert code == 0
        assert payload["recommendation"]
        assert payload["recommended_command"].startswith("ollama pull ")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_plan_json() -> None:
    root = make_workspace_temp_dir()
    try:
        (root / "module.py").write_text("print('hello')\n", encoding="utf-8")
        code, stdout, _ = run_cli(["plan", "module", "--path", str(root), "--json"])
        payload = json.loads(stdout)
        assert code == 0
        assert payload["selected_files"]
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_apply_dry_run_json() -> None:
    root = make_workspace_temp_dir()
    try:
        target = root / "module.py"
        target.write_text("print('hello')\n", encoding="utf-8")
        code, stdout, _ = run_cli(
            [
                "apply",
                "--path",
                str(root),
                "--file",
                "module.py",
                "--content",
                "print('bye')\n",
                "--dry-run",
                "--json",
            ]
        )
        payload = json.loads(stdout)
        assert code == 0
        assert payload["dry_run"] is True
        assert target.read_text(encoding="utf-8") == "print('hello')\n"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_test_command_json() -> None:
    root = make_workspace_temp_dir()
    try:
        code, stdout, _ = run_cli(
            [
                "test",
                "--path",
                str(root),
                "--command",
                "python -c \"print(456)\"",
                "--allow-shell",
                "--json",
            ]
        )
        payload = json.loads(stdout)
        assert code == 0
        assert "456" in payload["stdout"]
    finally:
        shutil.rmtree(root, ignore_errors=True)
