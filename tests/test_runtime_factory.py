"""Tests for runtime factory behavior."""

from __future__ import annotations

import pytest

from lordcoder.core.runtime import RuntimeNotImplementedError, create_runtime_adapter
from lordcoder.models import RuntimeSettings


def test_create_runtime_adapter_for_ollama() -> None:
    adapter = create_runtime_adapter(
        RuntimeSettings(provider="ollama", endpoint="http://127.0.0.1:11434/api", model="qwen2.5-coder:7b")
    )
    assert adapter.provider == "ollama"


def test_create_runtime_adapter_for_planned_runtime() -> None:
    with pytest.raises(RuntimeNotImplementedError):
        create_runtime_adapter(
            RuntimeSettings(provider="llama_cpp", endpoint="http://127.0.0.1:8080/v1", model="tiny.gguf")
        )
