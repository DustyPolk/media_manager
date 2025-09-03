"""
Media format detection for Media File Manager.

This module provides functionality to detect and validate
different media file formats.
"""

import magic
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FormatDetector:
    """
    Detects and validates media file formats.
    
    This class uses multiple methods to determine file types
    and validate their integrity.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize format detector with configuration.
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.supported_formats = config.get('supported_formats', [])
        
        # Initialize MIME type detection
        mimetypes.init()
        
    def detect_format(self, file_path: Path) -> Optional[str]:
        """
        Detect the format of a media file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Detected format string or None if detection failed
        """
        try:
            # Method 1: File extension
            extension = file_path.suffix.lower()
            if extension in self.supported_formats:
                return extension
                
            # Method 2: MIME type detection
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type:
                format_from_mime = self._mime_to_format(mime_type)
                if format_from_mime:
                    return format_from_mime
                    
            # Method 3: Magic number detection
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(1024)
                    magic_result = magic.from_buffer(header, mime=True)
                    format_from_magic = self._mime_to_format(magic_result)
                    if format_from_magic:
                        return format_from_magic
            except Exception as e:
                logger.debug(f"Magic detection failed for {file_path}: {e}")
                
            logger.warning(f"Could not detect format for {file_path}")
            return None
            
        except Exception as e:
            logger.error(f"Error detecting format for {file_path}: {e}")
            return None
            
    def validate_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate a media file for integrity and format.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Check if file exists and is readable
            if not file_path.exists():
                errors.append("File does not exist")
                return False, errors
                
            if not file_path.is_file():
                errors.append("Path is not a file")
                return False, errors
                
            # Check file size
            file_size = file_path.stat().st_size
            if file_size == 0:
                errors.append("File is empty")
                return False, errors
                
            # Check if file is readable
            try:
                with open(file_path, 'rb') as f:
                    f.read(1)
            except PermissionError:
                errors.append("File is not readable")
                return False, errors
                
            # Detect format
            detected_format = self.detect_format(file_path)
            if not detected_format:
                errors.append("Could not detect file format")
                return False, errors
                
            # Validate format-specific requirements
            format_errors = self._validate_format_specific(file_path, detected_format)
            errors.extend(format_errors)
            
            is_valid = len(errors) == 0
            return is_valid, errors
            
        except Exception as e:
            errors.append(f"Validation error: {e}")
            return False, errors
            
    def _mime_to_format(self, mime_type: str) -> Optional[str]:
        """
        Convert MIME type to file format.
        
        Args:
            mime_type: MIME type string
            
        Returns:
            File format extension or None
        """
        mime_to_format = {
            # Audio formats
            'audio/mpeg': '.mp3',
            'audio/flac': '.flac',
            'audio/wav': '.wav',
            'audio/aac': '.aac',
            'audio/ogg': '.ogg',
            'audio/mp4': '.m4a',
            
            # Video formats
            'video/mp4': '.mp4',
            'video/x-msvideo': '.avi',
            'video/x-matroska': '.mkv',
            'video/quicktime': '.mov',
            'video/x-ms-wmv': '.wmv',
            'video/x-flv': '.flv',
        }
        
        return mime_to_format.get(mime_type)
        
    def _validate_format_specific(self, file_path: Path, format_type: str) -> List[str]:
        """
        Validate format-specific requirements.
        
        Args:
            file_path: Path to the file
            format_type: Detected format type
            
        Returns:
            List of format-specific validation errors
        """
        errors = []
        
        try:
            if format_type in ['.mp3', '.flac', '.wav', '.aac', '.ogg', '.m4a']:
                # Audio format validation
                audio_errors = self._validate_audio_file(file_path, format_type)
                errors.extend(audio_errors)
            elif format_type in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']:
                # Video format validation
                video_errors = self._validate_video_file(file_path, format_type)
                errors.extend(video_errors)
                
        except Exception as e:
            errors.append(f"Format-specific validation error: {e}")
            
        return errors
        
    def _validate_audio_file(self, file_path: Path, format_type: str) -> List[str]:
        """Validate audio file format."""
        errors = []
        
        try:
            if format_type == '.mp3':
                # MP3 validation
                import mutagen
                try:
                    audio = mutagen.File(file_path)
                    if audio is None:
                        errors.append("Invalid MP3 file format")
                except Exception as e:
                    errors.append(f"MP3 validation failed: {e}")
                    
            elif format_type == '.flac':
                # FLAC validation
                import mutagen
                try:
                    audio = mutagen.File(file_path)
                    if audio is None:
                        errors.append("Invalid FLAC file format")
                except Exception as e:
                    errors.append(f"FLAC validation failed: {e}")
                    
            # Add more format-specific validation as needed
            
        except ImportError:
            errors.append(f"Required library not available for {format_type} validation")
            
        return errors
        
    def _validate_video_file(self, file_path: Path, format_type: str) -> List[str]:
        """Validate video file format."""
        errors = []
        
        try:
            # Basic video validation using ffmpeg
            import ffmpeg
            try:
                probe = ffmpeg.probe(str(file_path))
                if not probe or 'streams' not in probe:
                    errors.append("Invalid video file format")
                else:
                    # Check for video and audio streams
                    has_video = any(s['codec_type'] == 'video' for s in probe['streams'])
                    if not has_video:
                        errors.append("No video stream found")
                        
            except Exception as e:
                errors.append(f"Video validation failed: {e}")
                
        except ImportError:
            errors.append("FFmpeg library not available for video validation")
            
        return errors
