"""Runtime adapters for LordCoder."""

from __future__ import annotations

from ...models import RuntimeSettings
from .base import RuntimeAdapter
from .ollama import OllamaRuntimeAdapter


class RuntimeNotImplementedError(RuntimeError):
    """Raised when a planned runtime provider has not been implemented yet."""


def create_runtime_adapter(runtime: RuntimeSettings) -> RuntimeAdapter:
    """Create the configured runtime adapter."""
    if runtime.provider == "ollama":
        return OllamaRuntimeAdapter(endpoint=runtime.endpoint, model=runtime.model)
    if runtime.provider == "llama_cpp":
        raise RuntimeNotImplementedError(
            "Runtime provider 'llama_cpp' is planned but not implemented in this phase."
        )
    raise RuntimeNotImplementedError(
        f"Runtime provider '{runtime.provider}' is not supported."
    )
