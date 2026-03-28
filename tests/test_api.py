"""Tests for the local API router."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from lordcoder.core.api import LocalApiApplication


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"api-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_healthz() -> None:
    root = make_workspace_temp_dir()
    try:
        app = LocalApiApplication(root)
        response = app.handle("GET", "/healthz")
        assert response.status_code == 200
        assert response.payload["status"] == "ok"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_plan_endpoint() -> None:
    root = make_workspace_temp_dir()
    try:
        (root / "module.py").write_text("print('hello')\n", encoding="utf-8")
        app = LocalApiApplication(root)
        response = app.handle("POST", "/v1/plan", {"objective": "module", "max_files": 3})
        assert response.status_code == 200
        assert response.payload["scanned_files"] == 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_apply_endpoint_dry_run() -> None:
    root = make_workspace_temp_dir()
    try:
        (root / "module.py").write_text("print('hello')\n", encoding="utf-8")
        app = LocalApiApplication(root)
        response = app.handle(
            "POST",
            "/v1/apply",
            {
                "dry_run": True,
                "changes": [{"path": "module.py", "content": "print('bye')\n"}],
            },
        )
        assert response.status_code == 200
        assert response.payload["dry_run"] is True
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_test_endpoint() -> None:
    root = make_workspace_temp_dir()
    try:
        app = LocalApiApplication(root)
        response = app.handle(
            "POST",
            "/v1/test",
            {"command": "python -c \"print('ok')\"", "allow_shell": True},
        )
        assert response.status_code == 200
        assert response.payload["returncode"] == 0
    finally:
        shutil.rmtree(root, ignore_errors=True)
