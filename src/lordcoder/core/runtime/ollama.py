"""Ollama runtime adapter."""

from __future__ import annotations

import json
import shutil
import urllib.error
import urllib.request
from typing import Dict, List

from .base import RuntimeAdapter


class OllamaRuntimeAdapter(RuntimeAdapter):
    """Runtime adapter for a local Ollama instance."""

    provider = "ollama"

    def __init__(self, endpoint: str, model: str) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model

    def _request(self, path: str, payload: Dict[str, object] | None = None) -> Dict[str, object]:
        url = f"{self.endpoint}{path}"
        data = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(request, timeout=3) as response:
            raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}

    def is_available(self) -> bool:
        if shutil.which("ollama") is None:
            return False
        try:
            health = self.health()
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, ValueError):
            return False
        return bool(health.get("reachable"))

    def health(self) -> Dict[str, object]:
        try:
            models = self.list_models()
            return {"provider": self.provider, "reachable": True, "models": models}
        except urllib.error.URLError:
            return {"provider": self.provider, "reachable": False, "models": []}

    def list_models(self) -> List[str]:
        payload = self._request("/api/tags")
        models = payload.get("models", [])
        result: List[str] = []
        if isinstance(models, list):
            for item in models:
                if isinstance(item, dict) and "name" in item:
                    result.append(str(item["name"]))
        return result

    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, object]:
        return self._request(
            "/api/chat",
            payload={
                "model": self.model,
                "stream": False,
                "messages": messages,
            },
        )
