"""
File validation module for Media File Manager.

This module is responsible for validating media files.
"""

from typing import Dict, Any
from pathlib import Path

from media.format_detector import FormatDetector


class FileValidator:
    """
    Handles file validation operations.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the file validator."""
        self.config = config
        self.format_detector = FormatDetector(config)

    def validate_file(self, file_path: Path) -> bool:
        """Validate a media file."""
        is_valid, errors = self.format_detector.validate_file(file_path)
        if not is_valid:
            print(f"Warning: {file_path.name} is not a valid media file. Errors: {errors}")
        return is_valid
