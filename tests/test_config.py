"""Tests for config loading and legacy migration."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from lordcoder.config import load_config, save_config
from lordcoder.models import AppConfig


def make_workspace_temp_dir() -> Path:
    root = Path(".test-temp") / f"config-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_load_config_migrates_legacy_files() -> None:
    root = make_workspace_temp_dir()
    try:
        (root / "lordcoder.yml").write_text(
            "model: ollama/qwen2.5-coder:14b\nsystem-prompt: |\n  hello\n"
            "test-cmd: python -m pytest -q\n",
            encoding="utf-8",
        )
        (root / ".lordcoder-model").write_text("ollama/qwen2.5-coder:32b\n", encoding="utf-8")

        loaded = load_config(root)

        assert loaded.config.runtime.provider == "ollama"
        assert loaded.config.runtime.model == "qwen2.5-coder:32b"
        assert loaded.config.runtime.endpoint == "http://127.0.0.1:11434/api"
        assert loaded.config.project.test_command == "python -m pytest -q"
        assert any("system-prompt" in warning for warning in loaded.warnings)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_save_config_writes_toml() -> None:
    root = make_workspace_temp_dir()
    try:
        path = save_config(root, AppConfig())
        assert path.exists()
        loaded = load_config(root)
        assert loaded.source.endswith("lordcoder.toml")
        assert loaded.config.runtime.provider == "ollama"
    finally:
        shutil.rmtree(root, ignore_errors=True)
