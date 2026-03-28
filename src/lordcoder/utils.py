"""
System monitoring utilities for LordCoder.

This module provides utilities for monitoring system resources like
disk usage, memory, and CPU usage. Designed with proper error handling
and type hints for robust operation.
"""

import os
import platform
import shutil
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class DiskUsage:
    """Disk usage information for a path."""
    total: int  # Total bytes
    used: int   # Used bytes
    free: int   # Free bytes
    percent: float  # Usage percentage (0-100)
    path: str   # Path being measured


@dataclass
class MemoryInfo:
    """System memory information."""
    total: int  # Total bytes
    available: int  # Available bytes
    used: int   # Used bytes
    percent: float  # Usage percentage (0-100)
    swap_total: int  # Total swap bytes
    swap_used: int   # Used swap bytes
    swap_percent: float  # Swap usage percentage (0-100)


class SystemMonitor:
    """System monitoring utility class."""
    
    def __init__(self) -> None:
        """Initialize the system monitor."""
        self.platform = platform.system()
        self.psutil_available = PSUTIL_AVAILABLE
    
    def get_disk_usage(self, path: str = "/") -> DiskUsage:
        """
        Get disk usage information for a given path.
        
        Args:
            path: Path to check disk usage for
            
        Returns:
            DiskUsage object with usage information
            
        Raises:
            OSError: If the path doesn't exist or can't be accessed
        """
        if not os.path.exists(path):
            raise OSError(f"Path does not exist: {path}")
        
        try:
            if self.psutil_available:
                usage = psutil.disk_usage(path)
                return DiskUsage(
                    total=usage.total,
                    used=usage.used,
                    free=usage.free,
                    percent=round((usage.used / usage.total) * 100, 2),
                    path=path
                )
            else:
                # Fallback using shutil
                total, used, free = shutil.disk_usage(path)
                return DiskUsage(
                    total=total,
                    used=used,
                    free=free,
                    percent=round((used / total) * 100, 2),
                    path=path
                )
        except Exception as e:
            raise OSError(f"Failed to get disk usage for {path}: {e}")
    
    def get_memory_info(self) -> MemoryInfo:
        """
        Get system memory information.
        
        Returns:
            MemoryInfo object with memory usage information
            
        Raises:
            RuntimeError: If memory information cannot be retrieved
        """
        if not self.psutil_available:
            raise RuntimeError(
                "psutil is required for memory monitoring. "
                "Install with: pip install psutil"
            )
        
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return MemoryInfo(
                total=memory.total,
                available=memory.available,
                used=memory.used,
                percent=memory.percent,
                swap_total=swap.total,
                swap_used=swap.used,
                swap_percent=swap.percent
            )
        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}")
    
    def get_cpu_percent(self, interval: float = 1.0) -> float:
        """
        Get current CPU usage percentage.
        
        Args:
            interval: Time interval to measure CPU usage
            
        Returns:
            CPU usage percentage (0-100)
            
        Raises:
            RuntimeError: If CPU information cannot be retrieved
        """
        if not self.psutil_available:
            raise RuntimeError(
                "psutil is required for CPU monitoring. "
                "Install with: pip install psutil"
            )
        
        try:
            return psutil.cpu_percent(interval=interval)
        except Exception as e:
            raise RuntimeError(f"Failed to get CPU usage: {e}")
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get basic system information.
        
        Returns:
            Dictionary with system information
        """
        return {
            "platform": self.platform,
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }


def get_disk_usage(path: str = "/") -> DiskUsage:
    """
    Convenience function to get disk usage.
    
    Args:
        path: Path to check disk usage for
        
    Returns:
        DiskUsage object with usage information
    """
    monitor = SystemMonitor()
    return monitor.get_disk_usage(path)


def get_memory_info() -> MemoryInfo:
    """
    Convenience function to get memory information.
    
    Returns:
        MemoryInfo object with memory usage information
    """
    monitor = SystemMonitor()
    return monitor.get_memory_info()


def format_bytes(bytes_count: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_count: Number of bytes to format
        
    Returns:
        Human-readable string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"


def main() -> None:
    """Example usage of system monitoring utilities."""
    print("LordCoder System Monitor")
    print("=" * 40)
    
    monitor = SystemMonitor()
    
    # System info
    print("\nSystem Information:")
    for key, value in monitor.get_system_info().items():
        print(f"  {key}: {value}")
    
    # Disk usage
    try:
        disk_usage = monitor.get_disk_usage("/")
        print(f"\nDisk Usage ({disk_usage.path}):")
        print(f"  Total: {format_bytes(disk_usage.total)}")
        print(f"  Used:  {format_bytes(disk_usage.used)} ({disk_usage.percent}%)")
        print(f"  Free:  {format_bytes(disk_usage.free)}")
    except OSError as e:
        print(f"\nDisk usage error: {e}")
    
    # Memory info
    try:
        memory = monitor.get_memory_info()
        print(f"\nMemory Usage:")
        print(f"  Total:     {format_bytes(memory.total)}")
        print(f"  Used:      {format_bytes(memory.used)} ({memory.percent}%)")
        print(f"  Available: {format_bytes(memory.available)}")
        if memory.swap_total > 0:
            print(f"  Swap:      {format_bytes(memory.swap_used)} / {format_bytes(memory.swap_total)} ({memory.swap_percent}%)")
    except RuntimeError as e:
        print(f"\nMemory info error: {e}")
    
    # CPU usage
    try:
        cpu_percent = monitor.get_cpu_percent(interval=0.5)
        print(f"\nCPU Usage: {cpu_percent:.1f}%")
    except RuntimeError as e:
        print(f"\nCPU usage error: {e}")


if __name__ == "__main__":
    main()
