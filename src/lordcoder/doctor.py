"""Doctor diagnostics for LordCoder."""

from __future__ import annotations

import shutil
import urllib.error
from pathlib import Path
from typing import Dict, List

from .config import load_config
from .core.runtime.ollama import OllamaRuntimeAdapter
from .models import DoctorCheck, DoctorReport
from .utils import SystemMonitor, format_bytes


def normalize_arch(arch: str) -> str:
    """Normalise CPU architecture names."""
    mapping = {
        "amd64": "x64",
        "x86_64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
        "armv7l": "armv7",
        "armhf": "armv7",
    }
    return mapping.get(arch.lower(), arch.lower())


def recommend_model(ram_gb: float, arch: str) -> str:
    """Pick a safe default model tier."""
    normalised = normalize_arch(arch)
    if normalised == "armv7" or ram_gb < 8:
        return "qwen2.5-coder:1.5b"
    if ram_gb < 16:
        return "qwen2.5-coder:7b"
    if ram_gb < 32:
        return "qwen2.5-coder:14b"
    return "qwen2.5-coder:32b"


def build_doctor_report(project_root: Path) -> DoctorReport:
    """Build a doctor report for the current machine."""
    loaded = load_config(project_root)
    monitor = SystemMonitor()
    memory = monitor.get_memory_info()
    system = monitor.get_system_info()
    arch = normalize_arch(system["architecture"])
    runtime = loaded.config.runtime
    checks: List[DoctorCheck] = []

    checks.append(
        DoctorCheck(
            name="platform",
            status="PASS",
            message=f'{system["platform"]} {arch}',
            details={
                "python": system["python_version"],
                "ram": format_bytes(memory.total),
                "swap": format_bytes(memory.swap_total),
            },
        )
    )

    config_path = project_root / "lordcoder.toml"
    checks.append(
        DoctorCheck(
            name="config",
            status="PASS" if config_path.exists() else "WARN",
            message=f"Config source: {loaded.source}",
            details={"warnings": loaded.warnings},
        )
    )

    endpoint = runtime.endpoint.rstrip("/")
    if runtime.provider == "ollama":
        adapter = OllamaRuntimeAdapter(endpoint=endpoint, model=runtime.model)
        executable = shutil.which("ollama")
        status = "PASS" if executable else "WARN"
        message = f"Ollama executable found at {executable}" if executable else "Ollama executable not found on PATH"
        details: Dict[str, object] = {"endpoint": endpoint, "model": runtime.model}

        try:
            health = adapter.health()
            if bool(health.get("reachable")):
                details["models"] = health.get("models", [])
                checks.append(
                    DoctorCheck(
                        name="runtime",
                        status="PASS" if executable else "WARN",
                        message="Ollama runtime reachable on localhost",
                        details=details,
                    )
                )
            else:
                checks.append(
                    DoctorCheck(
                        name="runtime",
                        status="WARN",
                        message="Ollama runtime is not reachable on localhost",
                        details=details,
                    )
                )
        except (OSError, urllib.error.URLError):
            checks.append(DoctorCheck(name="runtime", status=status, message=message, details=details))
    else:
        checks.append(
            DoctorCheck(
                name="runtime",
                status="FAIL",
                message=f"Unsupported runtime provider: {runtime.provider}",
                details={"provider": runtime.provider},
            )
        )

    bind_status = "PASS" if loaded.config.daemon.host == "127.0.0.1" else "WARN"
    checks.append(
        DoctorCheck(
            name="daemon",
            status=bind_status,
            message=f'Daemon will bind to {loaded.config.daemon.host}:{loaded.config.daemon.port}',
            details={"host": loaded.config.daemon.host, "port": loaded.config.daemon.port},
        )
    )

    recommendation = recommend_model(memory.total / (1024 ** 3), arch)
    return DoctorReport(checks=checks, recommendation=recommendation, warnings=loaded.warnings)
