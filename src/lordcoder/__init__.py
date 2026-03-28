"""
LordCoder - Your local AI coding companion.

A powerful local AI coding assistant that provides intelligent multi-file editing,
automated testing, and seamless git integration.
"""

__version__ = "1.0.0"
__author__ = "Lovemore"
__email__ = "github@lvmre.dev"

from .utils import SystemMonitor, get_disk_usage, get_memory_info

__all__ = [
    "SystemMonitor",
    "get_disk_usage", 
    "get_memory_info",
]
