"""
Tests for LordCoder system monitoring utilities.

This test suite covers the core functionality of the utils module,
including error handling and edge cases.
"""

import os
import platform
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from src.lordcoder.utils import (
    SystemMonitor,
    DiskUsage,
    MemoryInfo,
    get_disk_usage,
    get_memory_info,
    format_bytes,
)


class TestSystemMonitor(unittest.TestCase):
    """Test cases for SystemMonitor class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.monitor = SystemMonitor()
    
    def test_init(self) -> None:
        """Test SystemMonitor initialization."""
        self.assertIsInstance(self.monitor, SystemMonitor)
        self.assertEqual(self.monitor.platform, platform.system())
        self.assertIsInstance(self.monitor.psutil_available, bool)
    
    def test_get_disk_usage_valid_path(self) -> None:
        """Test getting disk usage for a valid path."""
        # Test with current directory
        result = self.monitor.get_disk_usage(".")
        self.assertIsInstance(result, DiskUsage)
        self.assertGreater(result.total, 0)
        self.assertGreaterEqual(result.used, 0)
        self.assertGreaterEqual(result.free, 0)
        self.assertGreaterEqual(result.percent, 0)
        self.assertLessEqual(result.percent, 100)
        self.assertEqual(result.path, ".")
    
    def test_get_disk_usage_invalid_path(self) -> None:
        """Test getting disk usage for invalid path raises OSError."""
        with self.assertRaises(OSError):
            self.monitor.get_disk_usage("/nonexistent/path/12345")
    
    def test_get_disk_usage_temp_dir(self) -> None:
        """Test getting disk usage for temporary directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.monitor.get_disk_usage(temp_dir)
            self.assertIsInstance(result, DiskUsage)
            self.assertEqual(result.path, temp_dir)
    
    def test_format_bytes(self) -> None:
        """Test byte formatting function."""
        # Test various sizes
        self.assertEqual(format_bytes(0), "0.0 B")
        self.assertEqual(format_bytes(512), "512.0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1536), "1.5 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.0 MB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024 * 1024), "1.0 TB")
    
    def test_get_system_info(self) -> None:
        """Test getting system information."""
        info = self.monitor.get_system_info()
        self.assertIsInstance(info, dict)
        
        expected_keys = [
            "platform", "platform_release", "platform_version",
            "architecture", "hostname", "processor", "python_version"
        ]
        
        for key in expected_keys:
            self.assertIn(key, info)
            self.assertIsInstance(info[key], str)
    
    @patch('src.lordcoder.utils.PSUTIL_AVAILABLE', False)
    def test_memory_info_without_psutil(self) -> None:
        """Test that memory info raises RuntimeError without psutil."""
        monitor = SystemMonitor()
        with self.assertRaises(RuntimeError) as cm:
            monitor.get_memory_info()
        self.assertIn("psutil is required", str(cm.exception))
    
    @patch('src.lordcoder.utils.PSUTIL_AVAILABLE', False)
    def test_cpu_percent_without_psutil(self) -> None:
        """Test that CPU percent raises RuntimeError without psutil."""
        monitor = SystemMonitor()
        with self.assertRaises(RuntimeError) as cm:
            monitor.get_cpu_percent()
        self.assertIn("psutil is required", str(cm.exception))


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    def test_get_disk_usage_function(self) -> None:
        """Test get_disk_usage convenience function."""
        result = get_disk_usage(".")
        self.assertIsInstance(result, DiskUsage)
        self.assertGreater(result.total, 0)
    
    @patch('src.lordcoder.utils.PSUTIL_AVAILABLE', False)
    def test_get_memory_info_function_without_psutil(self) -> None:
        """Test get_memory_info function without psutil."""
        with self.assertRaises(RuntimeError):
            get_memory_info()


class TestDiskUsageDataclass(unittest.TestCase):
    """Test cases for DiskUsage dataclass."""
    
    def test_disk_usage_creation(self) -> None:
        """Test DiskUsage dataclass creation."""
        disk = DiskUsage(
            total=1000,
            used=500,
            free=500,
            percent=50.0,
            path="/test"
        )
        self.assertEqual(disk.total, 1000)
        self.assertEqual(disk.used, 500)
        self.assertEqual(disk.free, 500)
        self.assertEqual(disk.percent, 50.0)
        self.assertEqual(disk.path, "/test")
    
    def test_disk_usage_equality(self) -> None:
        """Test DiskUsage equality comparison."""
        disk1 = DiskUsage(1000, 500, 500, 50.0, "/test")
        disk2 = DiskUsage(1000, 500, 500, 50.0, "/test")
        disk3 = DiskUsage(1000, 600, 400, 60.0, "/test")
        
        self.assertEqual(disk1, disk2)
        self.assertNotEqual(disk1, disk3)


class TestMemoryInfoDataclass(unittest.TestCase):
    """Test cases for MemoryInfo dataclass."""
    
    def test_memory_info_creation(self) -> None:
        """Test MemoryInfo dataclass creation."""
        memory = MemoryInfo(
            total=8000,
            available=4000,
            used=4000,
            percent=50.0,
            swap_total=2000,
            swap_used=1000,
            swap_percent=50.0
        )
        self.assertEqual(memory.total, 8000)
        self.assertEqual(memory.available, 4000)
        self.assertEqual(memory.used, 4000)
        self.assertEqual(memory.percent, 50.0)
        self.assertEqual(memory.swap_total, 2000)
        self.assertEqual(memory.swap_used, 1000)
        self.assertEqual(memory.swap_percent, 50.0)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling."""
    
    def test_get_disk_usage_permission_error(self) -> None:
        """Test handling of permission errors."""
        monitor = SystemMonitor()
        
        # Mock os.path.exists to return True but shutil.disk_usage to raise error
        with patch('os.path.exists', return_value=True), \
             patch('shutil.disk_usage', side_effect=OSError("Permission denied")):
            with self.assertRaises(OSError) as cm:
                monitor.get_disk_usage("/restricted/path")
            # Check that some error message is present (may vary by OS)
            self.assertTrue(len(str(cm.exception)) > 0)
    
    def test_get_disk_usage_nonexistent_path(self) -> None:
        """Test handling of non-existent paths."""
        monitor = SystemMonitor()
        
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(OSError) as cm:
                monitor.get_disk_usage("/nonexistent/path")
            self.assertIn("does not exist", str(cm.exception))


class TestIntegration(unittest.TestCase):
    """Integration tests for the utils module."""
    
    def test_main_function_execution(self) -> None:
        """Test that main function runs without errors."""
        # Import main function and test it doesn't crash
        from src.lordcoder.utils import main
        
        # This should not raise any exceptions
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {e} unexpectedly!")
    
    def test_module_import(self) -> None:
        """Test that module imports work correctly."""
        from src.lordcoder import utils
        from src.lordcoder.utils import SystemMonitor, get_disk_usage, get_memory_info
        
        # Test that all expected items are available
        self.assertTrue(hasattr(utils, 'SystemMonitor'))
        self.assertTrue(hasattr(utils, 'get_disk_usage'))
        self.assertTrue(hasattr(utils, 'get_memory_info'))
        self.assertTrue(hasattr(utils, 'format_bytes'))


if __name__ == "__main__":
    unittest.main()
