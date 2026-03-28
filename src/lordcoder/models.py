"""Shared data models for LordCoder."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RuntimeSettings:
    """Runtime configuration."""

    provider: str = "ollama"
    endpoint: str = "http://127.0.0.1:11434/api"
    model: str = "qwen2.5-coder:7b"
    context_window: int = 8192


@dataclass
class RuntimeCapabilities:
    """Capabilities advertised by a runtime adapter."""

    streaming: bool = False
    model_management: bool = False
    structured_output: bool = False
    tool_calls: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialise runtime capabilities."""
        return asdict(self)


@dataclass
class ModelMetadata:
    """Lightweight model metadata exposed by runtimes."""

    name: str
    installed: bool
    context_window: Optional[int] = None
    size_bytes: Optional[int] = None
    family: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the model metadata."""
        return asdict(self)


@dataclass
class PermissionSettings:
    """Permission defaults for mutating actions."""

    allow_file_write: bool = False
    allow_shell: bool = False


@dataclass
class DaemonSettings:
    """Daemon bind settings."""

    host: str = "127.0.0.1"
    port: int = 32123


@dataclass
class ProjectSettings:
    """Project-scoped settings."""

    include: List[str] = field(default_factory=list)
    ignore: List[str] = field(
        default_factory=lambda: [
            ".git",
            ".venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
            ".test-temp",
            ".tmp-selector-test",
        ]
    )
    test_command: str = "python -m pytest -q"


@dataclass
class AppConfig:
    """Top-level application config."""

    runtime: RuntimeSettings = field(default_factory=RuntimeSettings)
    permissions: PermissionSettings = field(default_factory=PermissionSettings)
    daemon: DaemonSettings = field(default_factory=DaemonSettings)
    project: ProjectSettings = field(default_factory=ProjectSettings)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to a JSON-serialisable dictionary."""
        return asdict(self)


@dataclass
class LoadedConfig:
    """Config plus metadata about how it was loaded."""

    config: AppConfig
    source: str
    warnings: List[str] = field(default_factory=list)


@dataclass
class DoctorCheck:
    """One doctor check result."""

    name: str
    status: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the check."""
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class DoctorReport:
    """Aggregated doctor report."""

    checks: List[DoctorCheck]
    recommendation: str
    recommended_command: str
    warnings: List[str] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        """Return the highest-severity status."""
        if any(check.status == "FAIL" for check in self.checks):
            return "FAIL"
        if any(check.status == "WARN" for check in self.checks):
            return "WARN"
        return "PASS"

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the report."""
        return {
            "status": self.overall_status,
            "recommendation": self.recommendation,
            "recommended_command": self.recommended_command,
            "warnings": list(self.warnings),
            "checks": [check.to_dict() for check in self.checks],
        }


@dataclass
class FileIndexEntry:
    """Indexed file metadata."""

    path: str
    size: int
    modified_time: float
    score: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the index entry."""
        return {
            "path": self.path,
            "size": self.size,
            "modified_time": self.modified_time,
            "score": self.score,
        }


@dataclass
class PlanResponse:
    """Structured planning response."""

    objective: str
    target_path: str
    scanned_files: int
    selected_files: List[FileIndexEntry]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the plan."""
        return {
            "objective": self.objective,
            "target_path": self.target_path,
            "scanned_files": self.scanned_files,
            "selected_files": [entry.to_dict() for entry in self.selected_files],
            "summary": self.summary,
        }


@dataclass
class FileChange:
    """One file mutation request."""

    path: str
    content: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileChange":
        """Create a change from request data."""
        return cls(path=str(data["path"]), content=str(data["content"]))


@dataclass
class ApplyResponse:
    """Result of an apply operation."""

    dry_run: bool
    changed_files: List[str]
    diffs: Dict[str, str]
    written_files: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the apply result."""
        return {
            "dry_run": self.dry_run,
            "changed_files": list(self.changed_files),
            "diffs": dict(self.diffs),
            "written_files": list(self.written_files),
        }


@dataclass
class TestResponse:
    """Result of a test command."""

    command: List[str]
    returncode: int
    stdout: str
    stderr: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the test result."""
        return {
            "command": list(self.command),
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


@dataclass
class PluginManifest:
    """Basic plugin metadata."""

    name: str
    version: str
    capabilities: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the manifest."""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": list(self.capabilities),
        }


@dataclass
class ApiResponse:
    """Internal API response envelope."""

    status_code: int
    payload: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None
