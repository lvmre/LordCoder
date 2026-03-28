"""Lightweight local HTTP API."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict

from ..config import load_config
from ..models import ApiResponse, FileChange, PlanResponse
from .indexer import build_index, select_relevant_files
from .plugins import PluginManager
from .policy import PolicyError, PolicyManager


class LocalApiApplication:
    """Minimal JSON API router for localhost requests."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.loaded = load_config(project_root)
        self.plugins = PluginManager()
        self.plugins.register(self)

    def _policy(self) -> PolicyManager:
        config = self.loaded.config
        return PolicyManager(
            project_root=self.project_root,
            allow_file_write=config.permissions.allow_file_write,
            allow_shell=config.permissions.allow_shell,
        )

    def _handle_plan(self, payload: Dict[str, Any]) -> ApiResponse:
        objective = str(payload.get("objective", "")).strip()
        target_path = str(payload.get("path", "."))
        max_files = int(payload.get("max_files", 5))
        target_root = (self.project_root / target_path).resolve()
        entries = build_index(target_root, self.loaded.config.project.ignore)
        selected = select_relevant_files(entries, objective, max_files)
        response = PlanResponse(
            objective=objective,
            target_path=str(target_root),
            scanned_files=len(entries),
            selected_files=selected,
            summary=(
                f"Scanned {len(entries)} files and selected {len(selected)} files relevant "
                f"to '{objective or 'the project'}'."
            ),
        )
        return ApiResponse(status_code=HTTPStatus.OK, payload=response.to_dict())

    def _handle_apply(self, payload: Dict[str, Any]) -> ApiResponse:
        changes = [FileChange.from_dict(item) for item in payload.get("changes", [])]
        response = self._policy().apply_changes(
            changes=changes,
            dry_run=bool(payload.get("dry_run", False)),
            allow_write=bool(payload.get("allow_write", False)),
        )
        return ApiResponse(status_code=HTTPStatus.OK, payload=response.to_dict())

    def _handle_test(self, payload: Dict[str, Any]) -> ApiResponse:
        command = str(payload.get("command") or self.loaded.config.project.test_command)
        response = self._policy().run_test_command(
            command=command,
            cwd=self.project_root,
            allow_shell=bool(payload.get("allow_shell", False)),
        )
        return ApiResponse(status_code=HTTPStatus.OK, payload=response.to_dict())

    def handle(self, method: str, path: str, payload: Dict[str, Any] | None = None) -> ApiResponse:
        """Route a request to the appropriate handler."""
        payload = payload or {}
        if method == "GET" and path == "/healthz":
            return ApiResponse(
                status_code=HTTPStatus.OK,
                payload={
                    "status": "ok",
                    "config_source": self.loaded.source,
                    "runtime": self.loaded.config.runtime.provider,
                    "model": self.loaded.config.runtime.model,
                },
            )
        if method == "POST" and path == "/v1/plan":
            return self._handle_plan(payload)
        if method == "POST" and path == "/v1/apply":
            return self._handle_apply(payload)
        if method == "POST" and path == "/v1/test":
            return self._handle_test(payload)
        return ApiResponse(status_code=HTTPStatus.NOT_FOUND, payload={"error": "Not found"})


def create_request_handler(app: LocalApiApplication):
    """Build a request handler bound to an application instance."""

    class Handler(BaseHTTPRequestHandler):
        def _read_payload(self) -> Dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if not length:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw) if raw else {}

        def _write(self, response: ApiResponse) -> None:
            body = json.dumps(response.payload).encode("utf-8")
            self.send_response(int(response.status_code))
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            try:
                self._write(app.handle("GET", self.path))
            except PolicyError as exc:
                self._write(ApiResponse(status_code=HTTPStatus.FORBIDDEN, payload={"error": str(exc)}))

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self._read_payload()
                self._write(app.handle("POST", self.path, payload))
            except PolicyError as exc:
                self._write(ApiResponse(status_code=HTTPStatus.FORBIDDEN, payload={"error": str(exc)}))
            except json.JSONDecodeError:
                self._write(ApiResponse(status_code=HTTPStatus.BAD_REQUEST, payload={"error": "Invalid JSON"}))

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler
