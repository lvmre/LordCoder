"""Tests for policy and execution behavior."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from lordcoder.core.policy import PolicyError, PolicyManager
from lordcoder.models import FileChange


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"policy-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_apply_changes_dry_run_generates_diff() -> None:
    root = make_workspace_temp_dir()
    try:
        target = root / "hello.txt"
        target.write_text("before\n", encoding="utf-8")
        policy = PolicyManager(root, allow_file_write=False, allow_shell=False)
        result = policy.apply_changes([FileChange("hello.txt", "after\n")], dry_run=True, allow_write=False)
        assert "hello.txt" in result.diffs
        assert target.read_text(encoding="utf-8") == "before\n"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_apply_changes_requires_write_permission() -> None:
    root = make_workspace_temp_dir()
    try:
        policy = PolicyManager(root, allow_file_write=False, allow_shell=False)
        with pytest.raises(PolicyError):
            policy.apply_changes([FileChange("hello.txt", "after\n")], dry_run=False, allow_write=False)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_apply_changes_blocks_paths_outside_root() -> None:
    root = make_workspace_temp_dir()
    try:
        policy = PolicyManager(root, allow_file_write=True, allow_shell=False)
        with pytest.raises(PolicyError):
            policy.apply_changes([FileChange("../escape.txt", "bad\n")], dry_run=False, allow_write=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_run_test_command_requires_permission() -> None:
    root = make_workspace_temp_dir()
    try:
        policy = PolicyManager(root, allow_file_write=False, allow_shell=False)
        with pytest.raises(PolicyError):
            policy.run_test_command("python -c \"print('ok')\"", root, allow_shell=False)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_run_test_command_executes_when_allowed() -> None:
    root = make_workspace_temp_dir()
    try:
        policy = PolicyManager(root, allow_file_write=False, allow_shell=False)
        result = policy.run_test_command(
            "python -c \"print(123)\"",
            root,
            allow_shell=True,
        )
        assert result.returncode == 0
        assert "123" in result.stdout
    finally:
        shutil.rmtree(root, ignore_errors=True)
