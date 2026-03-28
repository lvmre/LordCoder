"""Configuration loading and persistence for LordCoder."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from .compat.legacy_config import load_legacy_config
from .models import AppConfig, LoadedConfig

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None


DEFAULT_CONFIG = AppConfig()


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _app_config_from_dict(data: Dict[str, Any]) -> AppConfig:
    runtime = data.get("runtime", {})
    permissions = data.get("permissions", {})
    daemon = data.get("daemon", {})
    project = data.get("project", {})
    return AppConfig(
        runtime=DEFAULT_CONFIG.runtime.__class__(**runtime),
        permissions=DEFAULT_CONFIG.permissions.__class__(**permissions),
        daemon=DEFAULT_CONFIG.daemon.__class__(**daemon),
        project=DEFAULT_CONFIG.project.__class__(**project),
    )


def _load_toml(path: Path) -> Dict[str, Any]:
    if tomllib is None:  # pragma: no cover
        raise RuntimeError("TOML parsing requires Python 3.11+ or tomli.")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    env_map = {
        "LORDCODER_RUNTIME_PROVIDER": ("runtime", "provider"),
        "LORDCODER_RUNTIME_ENDPOINT": ("runtime", "endpoint"),
        "LORDCODER_RUNTIME_MODEL": ("runtime", "model"),
        "LORDCODER_RUNTIME_CONTEXT_WINDOW": ("runtime", "context_window"),
        "LORDCODER_DAEMON_HOST": ("daemon", "host"),
        "LORDCODER_DAEMON_PORT": ("daemon", "port"),
        "LORDCODER_TEST_COMMAND": ("project", "test_command"),
        "LORDCODER_ALLOW_FILE_WRITE": ("permissions", "allow_file_write"),
        "LORDCODER_ALLOW_SHELL": ("permissions", "allow_shell"),
    }

    result = dict(config)
    for env_name, (section, key) in env_map.items():
        if env_name not in os.environ:
            continue
        section_values = dict(result.get(section, {}))
        raw_value = os.environ[env_name]
        if key in {"context_window", "port"}:
            section_values[key] = int(raw_value)
        elif key.startswith("allow_"):
            section_values[key] = raw_value.lower() == "true"
        else:
            section_values[key] = raw_value
        result[section] = section_values
    return result


def default_config_path(project_root: Path) -> Path:
    """Return the canonical config path."""
    return project_root / "lordcoder.toml"


def save_config(project_root: Path, config: AppConfig) -> Path:
    """Persist the config as TOML."""
    path = default_config_path(project_root)
    payload = config.to_dict()
    content = (
        "[runtime]\n"
        f'provider = "{payload["runtime"]["provider"]}"\n'
        f'endpoint = "{payload["runtime"]["endpoint"]}"\n'
        f'model = "{payload["runtime"]["model"]}"\n'
        f'context_window = {payload["runtime"]["context_window"]}\n\n'
        "[permissions]\n"
        f'allow_file_write = {str(payload["permissions"]["allow_file_write"]).lower()}\n'
        f'allow_shell = {str(payload["permissions"]["allow_shell"]).lower()}\n\n'
        "[daemon]\n"
        f'host = "{payload["daemon"]["host"]}"\n'
        f'port = {payload["daemon"]["port"]}\n\n'
        "[project]\n"
        f'include = {json.dumps(payload["project"]["include"])}\n'
        f'ignore = {json.dumps(payload["project"]["ignore"])}\n'
        f'test_command = "{payload["project"]["test_command"]}"\n'
    )
    path.write_text(content, encoding="utf-8")
    return path


def load_config(project_root: Path | None = None) -> LoadedConfig:
    """Load config from project files, legacy compatibility, and env."""
    root = project_root or Path.cwd()
    base = asdict(DEFAULT_CONFIG)
    warnings = []
    source = "defaults"

    config_path = default_config_path(root)
    if config_path.exists():
        loaded = _load_toml(config_path)
        base = _deep_merge(base, loaded)
        source = str(config_path)
    else:
        legacy = load_legacy_config(root)
        if legacy.config_overrides:
            base = _deep_merge(base, legacy.config_overrides)
            warnings.extend(legacy.warnings)
            source = str(legacy.source) if legacy.source else "legacy"

    base = _apply_env_overrides(base)
    return LoadedConfig(
        config=_app_config_from_dict(base),
        source=source,
        warnings=warnings,
    )
