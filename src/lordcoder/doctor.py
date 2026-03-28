"""Doctor diagnostics for LordCoder."""

from __future__ import annotations

import shutil
import urllib.error
from pathlib import Path
from typing import Dict, List

from .config import load_config
from .core.runtime import RuntimeNotImplementedError, create_runtime_adapter
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


def _model_rank(model: str) -> int:
    tiers = {
        "qwen2.5-coder:1.5b": 1,
        "qwen2.5-coder:7b": 2,
        "qwen2.5-coder:14b": 3,
        "qwen2.5-coder:32b": 4,
    }
    return tiers.get(model, 999)


def build_doctor_report(project_root: Path) -> DoctorReport:
    """Build a doctor report for the current machine."""
    loaded = load_config(project_root)
    monitor = SystemMonitor()
    memory = monitor.get_memory_info()
    system = monitor.get_system_info()
    arch = normalize_arch(system["architecture"])
    runtime = loaded.config.runtime
    checks: List[DoctorCheck] = []
    warnings = list(loaded.warnings)
    disk_usage = monitor.get_disk_usage(str(project_root))

    checks.append(
        DoctorCheck(
            name="platform",
            status="PASS",
            message=f'{system["platform"]} {arch}',
            details={
                "python": system["python_version"],
                "ram": format_bytes(memory.total),
                "swap": format_bytes(memory.swap_total),
                "disk_free": format_bytes(disk_usage.free),
                "disk_total": format_bytes(disk_usage.total),
            },
        )
    )

    config_path = project_root / "lordcoder.toml"
    checks.append(
        DoctorCheck(
            name="config",
            status="PASS" if config_path.exists() else "WARN",
            message=f"Config source: {loaded.source}",
            details={"warnings": loaded.warnings, "native_config": config_path.exists()},
        )
    )

    recommended_model = recommend_model(memory.total / (1024 ** 3), arch)
    recommended_command = f"ollama pull {recommended_model}"
    if _model_rank(runtime.model) > _model_rank(recommended_model):
        warnings.append(
            f"Configured model '{runtime.model}' is heavier than the recommended tier '{recommended_model}' for this machine."
        )

    try:
        adapter = create_runtime_adapter(runtime)
    except RuntimeNotImplementedError as exc:
        checks.append(
            DoctorCheck(
                name="runtime",
                status="WARN" if runtime.provider == "llama_cpp" else "FAIL",
                message=str(exc),
                details={
                    "provider": runtime.provider,
                    "endpoint": runtime.endpoint,
                    "model": runtime.model,
                },
            )
        )
    else:
        executable = shutil.which("ollama") if runtime.provider == "ollama" else None
        details: Dict[str, object] = {
            "provider": runtime.provider,
            "endpoint": runtime.endpoint,
            "model": runtime.model,
            "executable": executable,
            "capabilities": adapter.capabilities().to_dict(),
        }
        try:
            health = adapter.health()
        except (OSError, urllib.error.URLError) as exc:
            health = {"reachable": False, "error": str(exc), "recommended_command": adapter.ensure_model_command(runtime.model)}

        details.update(health)
        if health.get("configured_model_installed") is False:
            warnings.append(
                f"Configured model '{runtime.model}' is not currently installed."
            )
        status = "PASS"
        message = "Runtime reachable on localhost"
        if not executable and runtime.provider == "ollama":
            status = "WARN"
            message = "Ollama runtime reachable, but the ollama executable was not found on PATH"
        if not bool(health.get("reachable")):
            status = "WARN"
            message = "Configured runtime is not reachable on localhost"
        checks.append(
            DoctorCheck(
                name="runtime",
                status=status,
                message=message,
                details=details,
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

    return DoctorReport(
        checks=checks,
        recommendation=recommended_model,
        recommended_command=recommended_command,
        warnings=warnings,
    )
