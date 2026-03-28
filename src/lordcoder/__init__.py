"""
LordCoder - Your local AI coding companion.

A powerful local AI coding assistant that provides intelligent multi-file editing,
automated testing, and seamless git integration.
"""

__version__ = "1.0.0"
__author__ = "Lovemore"
__email__ = "github@lvmre.dev"

from .utils import SystemMonitor, get_disk_usage, get_memory_info
from .model_selector import (
    ModelSelection,
    choose_model,
    detect_provider,
    get_ollama_model_name,
    prepare_runtime_files,
    render_effective_config,
)

__all__ = [
    "ModelSelection",
    "SystemMonitor",
    "choose_model",
    "detect_provider",
    "get_disk_usage", 
    "get_ollama_model_name",
    "get_memory_info",
    "prepare_runtime_files",
    "render_effective_config",
]
