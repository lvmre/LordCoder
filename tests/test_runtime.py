"""Tests for runtime adapters."""

from __future__ import annotations

import io
import json
from unittest.mock import patch

from lordcoder.core.runtime.ollama import OllamaRuntimeAdapter
from lordcoder.models import RuntimeCapabilities


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


@patch("lordcoder.core.runtime.ollama.urllib.request.urlopen")
def test_list_models(mock_urlopen) -> None:
    mock_urlopen.return_value = _FakeResponse({"models": [{"name": "qwen2.5-coder:7b"}]})
    adapter = OllamaRuntimeAdapter("http://127.0.0.1:11434", "qwen2.5-coder:7b")
    assert adapter.list_models() == ["qwen2.5-coder:7b"]


@patch("lordcoder.core.runtime.ollama.urllib.request.urlopen")
def test_chat(mock_urlopen) -> None:
    mock_urlopen.return_value = _FakeResponse(
        {
            "message": {"content": "ok"},
            "eval_count": 10,
            "load_duration": 1,
            "eval_duration": 2,
        }
    )
    adapter = OllamaRuntimeAdapter("http://127.0.0.1:11434", "qwen2.5-coder:7b")
    response = adapter.chat([{"role": "user", "content": "hi"}])
    assert response["message"]["content"] == "ok"
    assert response["timings"]["load_duration"] == 1


@patch("lordcoder.core.runtime.ollama.shutil.which", return_value="ollama")
@patch("lordcoder.core.runtime.ollama.urllib.request.urlopen")
def test_is_available(mock_urlopen, _mock_which) -> None:
    mock_urlopen.return_value = _FakeResponse({"models": [{"name": "qwen2.5-coder:7b"}]})
    adapter = OllamaRuntimeAdapter("http://127.0.0.1:11434", "qwen2.5-coder:7b")
    assert adapter.is_available() is True


def test_capabilities() -> None:
    adapter = OllamaRuntimeAdapter("http://127.0.0.1:11434", "qwen2.5-coder:7b")
    capabilities = adapter.capabilities()
    assert isinstance(capabilities, RuntimeCapabilities)
    assert capabilities.streaming is True
    assert capabilities.model_management is True


@patch("lordcoder.core.runtime.ollama.urllib.request.urlopen")
def test_health_includes_install_guidance_for_missing_model(mock_urlopen) -> None:
    mock_urlopen.return_value = _FakeResponse({"models": [{"name": "qwen2.5-coder:7b"}]})
    adapter = OllamaRuntimeAdapter("http://127.0.0.1:11434", "qwen2.5-coder:14b")
    health = adapter.health()
    assert health["configured_model_installed"] is False
    assert "ollama pull qwen2.5-coder:14b" == health["recommended_command"]
