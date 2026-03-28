"""Daemon bootstrap for the local HTTP server."""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from pathlib import Path

from ..config import load_config
from .api import LocalApiApplication, create_request_handler


def run_daemon(project_root: Path, host: str | None = None, port: int | None = None) -> tuple[str, int]:
    """Run the local daemon until interrupted."""
    loaded = load_config(project_root)
    bind_host = host or loaded.config.daemon.host
    bind_port = port or loaded.config.daemon.port
    app = LocalApiApplication(project_root)
    server = ThreadingHTTPServer((bind_host, bind_port), create_request_handler(app))
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return bind_host, bind_port
