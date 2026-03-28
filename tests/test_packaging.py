"""Packaging smoke tests."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"packaging-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_pip_install_exposes_lordcoder_command() -> None:
    root = make_workspace_temp_dir()
    try:
        prefix = (root / "prefix").resolve()
        temp = (root / "tmp").resolve()
        prefix.mkdir()
        temp.mkdir()
        env = os.environ.copy()
        env["TMP"] = str(temp)
        env["TEMP"] = str(temp)
        env["TMPDIR"] = str(temp)
        install = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                ".",
                "--no-deps",
                "--prefix",
                str(prefix),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        if install.returncode != 0:
            combined = f"{install.stdout}\n{install.stderr}"
            if "Permission denied" in combined and "pip-build-tracker" in combined:
                pytest.skip("pip install smoke is blocked by temp-directory permissions in this environment")
            raise AssertionError(combined)

        scripts_dir = prefix / ("Scripts" if os.name == "nt" else "bin")
        candidates = [
            candidate
            for candidate in scripts_dir.glob("lordcoder*")
            if candidate.name.startswith("lordcoder") and "model" not in candidate.name
        ]
        assert candidates, "Expected a lordcoder entrypoint script"
        candidates.sort(key=lambda item: (item.suffix != ".exe", len(item.name)))
        command = [str(candidates[0]), "--version"]
        if candidates[0].suffix == ".py":
            command = [sys.executable, str(candidates[0]), "--version"]
        result = subprocess.run(command, check=True, capture_output=True, text=True, env=env)
        assert result.stdout.strip()
    finally:
        shutil.rmtree(root, ignore_errors=True)
