"""LordCoder package exports."""

__version__ = "1.1.0"
__author__ = "Lovemore"
__email__ = "github@lvmre.dev"

from .config import load_config, save_config
from .doctor import build_doctor_report, recommend_model
from .model_selector import (
    ModelSelection,
    choose_model,
    detect_provider,
    get_ollama_model_name,
    prepare_runtime_files,
    render_effective_config,
)
from .utils import SystemMonitor, get_disk_usage, get_memory_info

__all__ = [
    "ModelSelection",
    "SystemMonitor",
    "build_doctor_report",
    "choose_model",
    "detect_provider",
    "get_disk_usage",
    "get_ollama_model_name",
    "get_memory_info",
    "load_config",
    "prepare_runtime_files",
    "recommend_model",
    "render_effective_config",
    "save_config",
]
