"""
File renaming module for Media File Manager.

This module is responsible for generating new filenames based on metadata
and performing the renaming operation.
"""

from typing import Dict, Any
from pathlib import Path

from utils.file_utils import sanitize_filename, get_unique_filename


class FileRenamer:
    """
    Handles file renaming operations.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the file renamer."""
        self.config = config

    def generate_filename(self, file_path: Path, metadata: Dict[str, Any]) -> str:
        """Generate a new filename based on metadata."""
        if self._is_audio(file_path):
            pattern = self.config.get("naming", {}).get("audio_pattern", "{artist} - {title}")
        elif self._is_video(file_path):
            pattern = self.config.get("naming", {}).get("video_pattern", "{title} ({year})")
        else:
            return file_path.name

        try:
            new_name = pattern.format(**metadata)
        except KeyError as e:
            print(f"Warning: Metadata key {e} not found for {file_path.name}")
            return file_path.name

        return sanitize_filename(f"{new_name}{file_path.suffix}")

    def rename_file(self, old_path: Path, new_name: str) -> Path:
        """Rename a file."""
        new_path = old_path.parent / new_name
        new_path = get_unique_filename(new_path)
        old_path.rename(new_path)
        return new_path

    def _is_audio(self, file_path: Path) -> bool:
        """Check if a file is an audio file."""
        return file_path.suffix.lower() in self.config.get("supported_formats", {}).get(
            "audio", []
        )

    def _is_video(self, file_path: Path) -> bool:
        """Check if a file is a video file."""
        return file_path.suffix.lower() in self.config.get("supported_formats", {}).get(
            "video", []
        )
