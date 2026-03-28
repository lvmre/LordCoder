"""Runtime abstraction for LordCoder."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class RuntimeAdapter(ABC):
    """Abstract runtime interface."""

    provider: str

    @abstractmethod
    def is_available(self) -> bool:
        """Return whether the runtime looks reachable."""

    @abstractmethod
    def health(self) -> Dict[str, object]:
        """Return a health payload."""

    @abstractmethod
    def list_models(self) -> List[str]:
        """List models known to the runtime."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, object]:
        """Execute a non-streaming chat request."""
