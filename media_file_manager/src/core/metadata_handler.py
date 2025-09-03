"""
Metadata handling module for Media File Manager.

This module is responsible for extracting, processing, and updating
metadata in media files.
"""

from typing import Dict, Any
from pathlib import Path

from media.audio_processor import AudioProcessor
from media.video_processor import VideoProcessor


class MetadataHandler:
    """
    Handles metadata extraction and updates for media files.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the metadata handler."""
        self.config = config
        self.audio_processor = AudioProcessor(config)
        self.video_processor = VideoProcessor(config)

    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from a media file."""
        if self._is_audio(file_path):
            return self.audio_processor.extract_metadata(file_path)
        elif self._is_video(file_path):
            return self.video_processor.extract_metadata(file_path)
        return {}

    def update_metadata(self, file_path: Path, metadata: Dict[str, Any]) -> bool:
        """Update metadata in a media file."""
        if self._is_audio(file_path):
            return self.audio_processor.update_metadata(file_path, metadata)
        elif self._is_video(file_path):
            return self.video_processor.update_metadata(file_path, metadata)
        return False

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
