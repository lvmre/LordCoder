"""Plugin loading for LordCoder."""

from __future__ import annotations

from importlib import metadata
from typing import Any, List, Protocol

from ..models import PluginManifest


class Plugin(Protocol):
    """Basic plugin protocol."""

    manifest: PluginManifest

    def register(self, app: Any) -> None:
        """Register the plugin with the application."""


class PluginManager:
    """Discover and register in-process plugins."""

    def discover(self) -> List[Plugin]:
        plugins: List[Plugin] = []
        for entry_point in metadata.entry_points().select(group="lordcoder.plugins"):
            loaded = entry_point.load()
            plugin = loaded() if callable(loaded) else loaded
            plugins.append(plugin)
        return plugins

    def manifests(self) -> List[PluginManifest]:
        """Return discovered plugin manifests."""
        manifests: List[PluginManifest] = []
        for plugin in self.discover():
            manifest = getattr(plugin, "manifest", None)
            if isinstance(manifest, PluginManifest):
                manifests.append(manifest)
        return manifests

    def register(self, app: Any) -> None:
        """Register all discovered plugins."""
        for plugin in self.discover():
            plugin.register(app)
