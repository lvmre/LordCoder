"""Tests for doctor diagnostics."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from lordcoder.doctor import build_doctor_report, normalize_arch, recommend_model


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"doctor-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_normalize_arch() -> None:
    assert normalize_arch("x86_64") == "x64"
    assert normalize_arch("aarch64") == "arm64"
    assert normalize_arch("armv7l") == "armv7"


def test_recommend_model() -> None:
    assert recommend_model(4, "armv7") == "qwen2.5-coder:1.5b"
    assert recommend_model(12, "x86_64") == "qwen2.5-coder:7b"
    assert recommend_model(24, "x86_64") == "qwen2.5-coder:14b"


def test_build_doctor_report_includes_config_warnings() -> None:
    root = make_workspace_temp_dir()
    try:
        (root / "lordcoder.yml").write_text(
            "model: ollama/qwen2.5-coder:14b\nsystem-prompt: |\n  legacy\n",
            encoding="utf-8",
        )
        report = build_doctor_report(root)
        assert report.recommendation
        assert report.checks
        assert any("system-prompt" in warning for warning in report.warnings)
    finally:
        shutil.rmtree(root, ignore_errors=True)
