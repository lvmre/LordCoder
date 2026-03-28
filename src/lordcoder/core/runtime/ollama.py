"""Ollama runtime adapter."""

from __future__ import annotations

import json
import shutil
import urllib.error
import urllib.request
from typing import Dict, List

from ...models import ModelMetadata, RuntimeCapabilities
from .base import RuntimeAdapter


class OllamaRuntimeAdapter(RuntimeAdapter):
    """Runtime adapter for a local Ollama instance."""

    provider = "ollama"

    def __init__(self, endpoint: str, model: str) -> None:
        self.endpoint = self._normalize_endpoint(endpoint)
        self.model = model

    @staticmethod
    def _normalize_endpoint(endpoint: str) -> str:
        normalized = endpoint.rstrip("/")
        if normalized.endswith("/api"):
            return normalized
        return f"{normalized}/api"

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

    def capabilities(self) -> RuntimeCapabilities:
        return RuntimeCapabilities(
            streaming=True,
            model_management=True,
            structured_output=False,
            tool_calls=False,
        )

    def health(self) -> Dict[str, object]:
        try:
            models = self.list_models()
            model_names = set(models)
            model_present = self.model in model_names
            return {
                "provider": self.provider,
                "endpoint": self.endpoint,
                "reachable": True,
                "models": models,
                "configured_model_installed": model_present,
                "recommended_command": None if model_present else self.ensure_model_command(self.model),
                "capabilities": self.capabilities().to_dict(),
            }
        except urllib.error.HTTPError as exc:
            return {
                "provider": self.provider,
                "endpoint": self.endpoint,
                "reachable": False,
                "models": [],
                "error": f"HTTP {exc.code}",
                "recommended_command": self.ensure_model_command(self.model),
                "capabilities": self.capabilities().to_dict(),
            }
        except urllib.error.URLError as exc:
            return {
                "provider": self.provider,
                "endpoint": self.endpoint,
                "reachable": False,
                "models": [],
                "error": str(exc.reason),
                "recommended_command": self.ensure_model_command(self.model),
                "capabilities": self.capabilities().to_dict(),
            }

    def list_models(self) -> List[str]:
        payload = self._request("/tags")
        models = payload.get("models", [])
        result: List[str] = []
        if isinstance(models, list):
            for item in models:
                if isinstance(item, dict) and "name" in item:
                    result.append(str(item["name"]))
        return result

    def model_metadata(self, model: str) -> ModelMetadata:
        payload = self._request("/tags")
        models = payload.get("models", [])
        if isinstance(models, list):
            for item in models:
                if isinstance(item, dict) and str(item.get("name")) == model:
                    return ModelMetadata(
                        name=model,
                        installed=True,
                        size_bytes=int(item["size"]) if isinstance(item.get("size"), int) else None,
                        family=str(item.get("details", {}).get("family")) if isinstance(item.get("details"), dict) else None,
                    )
        return ModelMetadata(name=model, installed=False)

    def ensure_model_command(self, model: str) -> str:
        return f"ollama pull {model}"

    def chat(self, messages: List[Dict[str, str]], *, stream: bool = False) -> Dict[str, object]:
        response = self._request(
            "/chat",
            payload={
                "model": self.model,
                "stream": stream,
                "messages": messages,
            },
        )
        timings = {}
        for key in ("total_duration", "load_duration", "prompt_eval_duration", "eval_duration"):
            if key in response:
                timings[key] = response[key]
        if timings:
            response["timings"] = timings
        return response
