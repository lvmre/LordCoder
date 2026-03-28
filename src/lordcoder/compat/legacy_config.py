"""Compatibility helpers for the legacy LordCoder config files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class LegacyConfigMigration:
    """Result of inspecting legacy config files."""

    config_overrides: Dict[str, object] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    source: Optional[Path] = None


def _coerce_scalar(value: str) -> object:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        return value


def _parse_legacy_yaml(path: Path) -> Dict[str, object]:
    parsed: Dict[str, object] = {}
    current_block_key: Optional[str] = None
    block_lines: List[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if current_block_key:
            if raw_line.startswith("  "):
                block_lines.append(raw_line[2:])
                continue
            parsed[current_block_key] = "\n".join(block_lines)
            current_block_key = None
            block_lines = []

        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in raw_line:
            continue

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "|":
            current_block_key = key
            block_lines = []
            continue
        parsed[key] = _coerce_scalar(value)

    if current_block_key:
        parsed[current_block_key] = "\n".join(block_lines)
    return parsed


def load_legacy_config(project_root: Path) -> LegacyConfigMigration:
    """Load the checked-in legacy config and state files if present."""
    legacy_path = project_root / "lordcoder.yml"
    state_path = project_root / ".lordcoder-model"
    result = LegacyConfigMigration()

    if legacy_path.exists():
        legacy_values = _parse_legacy_yaml(legacy_path)
        result.source = legacy_path

        runtime: Dict[str, object] = {}
        project: Dict[str, object] = {}

        model = legacy_values.get("model")
        if isinstance(model, str) and model:
            if "/" in model:
                provider, model_name = model.split("/", 1)
                runtime["provider"] = provider
                runtime["model"] = model_name
                if provider == "ollama":
                    runtime["endpoint"] = "http://127.0.0.1:11434/api"
            else:
                runtime["model"] = model

        if "test-cmd" in legacy_values:
            project["test_command"] = legacy_values["test-cmd"]

        if "system-prompt" in legacy_values:
            result.warnings.append(
                "Legacy key 'system-prompt' is not supported by the native LordCoder core and was ignored."
            )

        if "auto-commits" in legacy_values:
            result.warnings.append(
                "Legacy key 'auto-commits' was detected. Native git automation is not implemented in phase 1."
            )

        if "git" in legacy_values:
            result.warnings.append(
                "Legacy key 'git' was detected. Native git automation is not implemented in phase 1."
            )

        if runtime:
            result.config_overrides["runtime"] = runtime
        if project:
            result.config_overrides["project"] = project

    if state_path.exists():
        saved_model = state_path.read_text(encoding="utf-8").strip()
        if saved_model:
            runtime = dict(result.config_overrides.get("runtime", {}))
            if "/" in saved_model:
                provider, model_name = saved_model.split("/", 1)
                runtime["provider"] = provider
                runtime["model"] = model_name
                if provider == "ollama":
                    runtime["endpoint"] = "http://127.0.0.1:11434/api"
            else:
                runtime["model"] = saved_model
            result.config_overrides["runtime"] = runtime
            result.warnings.append(
                "Migrated model selection from .lordcoder-model into the runtime configuration."
            )

    return result
