"""
CLI commands for Media File Manager.
"""

from pathlib import Path
from typing import Dict, Any

from core.file_processor import FileProcessor


def process_files(path: Path, config: Dict[str, Any]):
    """Process media files in the specified path."""
    file_processor = FileProcessor(config)
    if path.is_dir():
        file_processor.process_directory(path)
    else:
        file_processor.process_file(path)


def preview_changes(path: Path, config: Dict[str, Any]):
    """Preview changes that would be made without applying them."""
    # This will be implemented later
    print("Previewing changes is not yet implemented.")


def restore_backup(backup_path: Path):
    """Restore files from a backup."""
    # This will be implemented later
    print("Restoring from backup is not yet implemented.")


def show_info():
    """Show application information and configuration."""
    # This will be implemented later
    print("Showing info is not yet implemented.")
