"""Runtime abstraction for LordCoder."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from ...models import ModelMetadata, RuntimeCapabilities

class RuntimeAdapter(ABC):
    """Abstract runtime interface."""

    provider: str

    @abstractmethod
    def is_available(self) -> bool:
        """Return whether the runtime looks reachable."""

    @abstractmethod
    def capabilities(self) -> RuntimeCapabilities:
        """Return the runtime capabilities."""

    @abstractmethod
    def health(self) -> Dict[str, object]:
        """Return a health payload."""

    @abstractmethod
    def list_models(self) -> List[str]:
        """List models known to the runtime."""

    @abstractmethod
    def model_metadata(self, model: str) -> ModelMetadata:
        """Return metadata for a model."""

    @abstractmethod
    def ensure_model_command(self, model: str) -> str:
        """Return a user-facing command to install or fetch a model."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], *, stream: bool = False) -> Dict[str, object]:
        """Execute a chat request."""
