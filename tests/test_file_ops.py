"""Tests for FileOperations."""

import pytest
import tempfile
import os
from pathlib import Path
from ollamacode.tools import FileOperations


def test_read_file_success():
    """Test successful file reading."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Hello, world!")
        temp_path = f.name
    
    try:
        content = FileOperations.read_file(temp_path)
        assert content == "Hello, world!"
    finally:
        os.unlink(temp_path)


def test_read_file_not_exists():
    """Test reading a non-existent file."""
    content = FileOperations.read_file("/nonexistent/file.txt")
    assert content is None


def test_write_file_success():
    """Test successful file writing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test.txt")
        
        success = FileOperations.write_file(file_path, "Test content")
        assert success is True
        
        with open(file_path, 'r') as f:
            assert f.read() == "Test content"


def test_list_files():
    """Test file listing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        Path(os.path.join(temp_dir, "test1.py")).touch()
        Path(os.path.join(temp_dir, "test2.py")).touch()
        Path(os.path.join(temp_dir, "test.txt")).touch()
        
        # Test listing Python files
        py_files = FileOperations.list_files(temp_dir, "*.py")
        assert len(py_files) == 2
        assert all(f.endswith('.py') for f in py_files)
        
        # Test listing all files
        all_files = FileOperations.list_files(temp_dir, "*")
        assert len(all_files) == 3


def test_get_file_info():
    """Test file info retrieval."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        info = FileOperations.get_file_info(temp_path)
        assert info is not None
        assert info['is_file'] is True
        assert info['is_dir'] is False
        assert info['size'] > 0
        assert 'path' in info
        assert 'modified' in info
    finally:
        os.unlink(temp_path)