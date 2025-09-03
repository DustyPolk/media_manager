# Media File Manager - Implementation Roadmap

## Development Timeline: 8 Weeks

This roadmap provides a detailed, step-by-step guide for implementing the Media File Manager project. Each phase includes specific implementation details, code examples, and testing strategies.

---

## Phase 1: Core Infrastructure (Week 1-2)

### Week 1: Project Setup and Basic Structure

#### Day 1-2: Project Initialization
```bash
# Create project structure
mkdir -p media_file_manager/{src/{core,media,utils,cli},tests/{test_core,test_media,test_utils,test_cli},config,docs,scripts}

# Initialize Python project
cd media_file_manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
```

#### Day 3-4: Dependencies and Configuration
```bash
# Install core dependencies
pip install mutagen Pillow ffmpeg-python python-magic PyYAML click tqdm colorama

# Install development dependencies
pip install pytest pytest-cov pytest-mock black flake8 mypy pylint
```

#### Day 5-7: Basic File Structure Implementation

**1. Create `pyproject.toml`**
```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "media-file-manager"
version = "1.0.0"
description = "Automated media file organization and metadata management"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "mutagen>=1.46.0",
    "Pillow>=9.0.0",
    "ffmpeg-python>=0.2.0",
    "python-magic>=0.4.27",
    "PyYAML>=6.0",
    "click>=8.0.0",
    "tqdm>=4.64.0",
    "colorama>=0.4.5",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
    "mypy>=0.991",
    "pylint>=2.15.0",
]

[project.scripts]
media-manager = "media_file_manager.main:main"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

**2. Create `setup.py`**
```python
#!/usr/bin/env python3
"""Setup script for Media File Manager."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="media-file-manager",
        version="1.0.0",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        python_requires=">=3.8",
        install_requires=[
            "mutagen>=1.46.0",
            "Pillow>=9.0.0",
            "ffmpeg-python>=0.2.0",
            "python-magic>=0.4.27",
            "PyYAML>=6.0",
            "click>=8.0.0",
            "tqdm>=4.64.0",
            "colorama>=0.4.5",
        ],
        extras_require={
            "dev": [
                "pytest>=7.0.0",
                "pytest-cov>=4.0.0",
                "pytest-mock>=3.10.0",
                "black>=22.0.0",
                "flake8>=5.0.0",
                "mypy>=0.991",
                "pylint>=2.15.0",
            ]
        },
        entry_points={
            "console_scripts": [
                "media-manager=media_file_manager.main:main",
            ],
        },
        author="Your Name",
        author_email="your.email@example.com",
        description="Automated media file organization and metadata management",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/username/media-file-manager",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Video",
            "Topic :: Utilities",
        ],
    )
```

**3. Create basic `__init__.py` files**
```python
# src/__init__.py
"""Media File Manager - Automated media file organization and metadata management."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from . import core, media, utils, cli

__all__ = ["core", "media", "utils", "cli"]
```

### Week 2: Core Utilities and Configuration

#### Day 1-3: Configuration Management

**1. Implement `src/utils/config.py`** (Complete implementation from project structure guide)

**2. Create configuration files**
```yaml
# config/default_config.yaml
# (Complete implementation from project structure guide)

# config/user_config.yaml
# (Complete implementation from project structure guide)
```

#### Day 4-5: Logging System

**1. Implement `src/utils/logger.py`**
```python
"""
Logging utilities for Media File Manager.

This module provides centralized logging configuration and utilities
for consistent logging across the application.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Optional custom log format
        config: Optional configuration dictionary
    """
    # Get configuration
    if config:
        level = config.get('logging', {}).get('level', level)
        log_file = config.get('logging', {}).get('file', log_file)
        log_format = config.get('logging', {}).get('format', log_format)
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(log_format)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file).expanduser().resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger('mutagen').setLevel(logging.WARNING)
    logging.getLogger('ffmpeg').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_function_call(func):
    """Decorator to log function calls with parameters."""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise
    return wrapper
```

#### Day 6-7: File Utilities and Backup System

**1. Implement `src/utils/file_utils.py`**
```python
"""
File utility functions for Media File Manager.

This module provides common file operations and utilities used
throughout the application.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)


def safe_path(path: Union[str, Path]) -> Path:
    """
    Convert path to Path object and resolve to absolute path.
    
    Args:
        path: Path string or Path object
        
    Returns:
        Resolved Path object
        
    Raises:
        ValueError: If path is invalid or doesn't exist
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        raise ValueError(f"Path does not exist: {path_obj}")
        
    return path_obj


def is_media_file(file_path: Path, supported_formats: List[str]) -> bool:
    """
    Check if a file is a supported media format.
    
    Args:
        file_path: Path to the file
        supported_formats: List of supported file extensions
        
    Returns:
        True if file is a supported media format
    """
    if not file_path.is_file():
        return False
        
    return file_path.suffix.lower() in supported_formats


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    try:
        return file_path.stat().st_size
    except OSError as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0


def calculate_file_hash(file_path: Path, algorithm: str = "md5") -> Optional[str]:
    """
    Calculate hash of file content.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use
        
    Returns:
        Hexadecimal hash string or None if error
    """
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return None


def create_directory_safe(directory_path: Path) -> bool:
    """
    Create directory safely, handling existing directories.
    
    Args:
        directory_path: Path to create
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory_path}: {e}")
        return False


def copy_file_safe(source: Path, destination: Path, overwrite: bool = False) -> bool:
    """
    Copy file safely with error handling.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
        
    Returns:
        True if copy was successful
    """
    try:
        if destination.exists() and not overwrite:
            logger.warning(f"Destination file exists and overwrite=False: {destination}")
            return False
            
        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(source, destination)
        logger.info(f"Successfully copied {source} to {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Error copying {source} to {destination}: {e}")
        return False


def move_file_safe(source: Path, destination: Path, overwrite: bool = False) -> bool:
    """
    Move file safely with error handling.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
        
    Returns:
        True if move was successful
    """
    try:
        if destination.exists() and not overwrite:
            logger.warning(f"Destination file exists and overwrite=False: {destination}")
            return False
            
        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(source), str(destination))
        logger.info(f"Successfully moved {source} to {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Error moving {source} to {destination}: {e}")
        return False


def find_media_files(
    directory_path: Path,
    supported_formats: List[str],
    recursive: bool = True
) -> List[Path]:
    """
    Find all media files in a directory.
    
    Args:
        directory_path: Directory to search
        supported_formats: List of supported file extensions
        recursive: Whether to search subdirectories
        
    Returns:
        List of media file paths
    """
    media_files = []
    
    try:
        if recursive:
            search_pattern = "**/*"
        else:
            search_pattern = "*"
            
        for file_path in directory_path.glob(search_pattern):
            if file_path.is_file() and is_media_file(file_path, supported_formats):
                media_files.append(file_path)
                
        logger.info(f"Found {len(media_files)} media files in {directory_path}")
        return media_files
        
    except Exception as e:
        logger.error(f"Error searching for media files in {directory_path}: {e}")
        return []


def sanitize_filename(filename: str, replace_chars: str = "_") -> str:
    """
    Sanitize filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        replace_chars: Character to replace invalid characters with
        
    Returns:
        Sanitized filename
    """
    # Characters that are invalid in most file systems
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters
    for char in invalid_chars:
        filename = filename.replace(char, replace_chars)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
        
    return filename


def get_unique_filename(file_path: Path) -> Path:
    """
    Generate a unique filename if the original already exists.
    
    Args:
        file_path: Original file path
        
    Returns:
        Unique file path
    """
    if not file_path.exists():
        return file_path
        
    counter = 1
    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent
    
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1
```

**2. Implement `src/utils/backup.py`**
```python
"""
Backup management for Media File Manager.

This module handles creating, managing, and restoring backups
of media files before processing.
"""

import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Manages backup operations for media files.
    
    This class handles creating backups before file modifications,
    tracking backup metadata, and providing restore functionality.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize backup manager with configuration.
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.backup_dir = Path(config.get('processing', {}).get('backup_directory', './backups'))
        self.backup_enabled = config.get('processing', {}).get('backup_enabled', True)
        
        # Ensure backup directory exists
        if self.backup_enabled:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
        # Backup metadata file
        self.metadata_file = self.backup_dir / "backup_metadata.json"
        self.backup_metadata = self._load_backup_metadata()
        
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of the specified file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to backup file or None if backup failed
        """
        if not self.backup_enabled:
            logger.debug("Backup disabled, skipping backup creation")
            return None
            
        try:
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_filename
            
            # Create backup
            shutil.copy2(file_path, backup_path)
            
            # Update metadata
            self._add_backup_entry(file_path, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup for {file_path}: {e}")
            return None
            
    def restore_backup(self, backup_path: Path, restore_path: Optional[Path] = None) -> bool:
        """
        Restore a file from backup.
        
        Args:
            backup_path: Path to the backup file
            restore_path: Path to restore to (defaults to original location)
            
        Returns:
            True if restore was successful
        """
        try:
            # Find original file path from metadata
            original_path = self._get_original_path(backup_path)
            
            if not original_path:
                logger.error(f"No metadata found for backup: {backup_path}")
                return False
                
            # Determine restore path
            if restore_path is None:
                restore_path = original_path
                
            # Ensure restore directory exists
            restore_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Restore file
            shutil.copy2(backup_path, restore_path)
            
            logger.info(f"Restored {backup_path} to {restore_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore from backup {backup_path}: {e}")
            return False
            
    def list_backups(self, file_path: Optional[Path] = None) -> List[Dict]:
        """
        List available backups.
        
        Args:
            file_path: Optional file path to filter backups
            
        Returns:
            List of backup information dictionaries
        """
        if file_path:
            return [entry for entry in self.backup_metadata 
                   if entry.get('original_path') == str(file_path)]
        else:
            return self.backup_metadata.copy()
            
    def cleanup_old_backups(self, max_age_days: int = 30) -> int:
        """
        Remove old backup files.
        
        Args:
            max_age_days: Maximum age of backups to keep
            
        Returns:
            Number of backups removed
        """
        if not self.backup_enabled:
            return 0
            
        removed_count = 0
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)
        
        for entry in self.backup_metadata[:]:
            backup_path = Path(entry['backup_path'])
            if backup_path.exists():
                if backup_path.stat().st_mtime < cutoff_time:
                    try:
                        backup_path.unlink()
                        self.backup_metadata.remove(entry)
                        removed_count += 1
                        logger.info(f"Removed old backup: {backup_path}")
                    except Exception as e:
                        logger.error(f"Failed to remove old backup {backup_path}: {e}")
                        
        # Save updated metadata
        self._save_backup_metadata()
        
        return removed_count
        
    def _load_backup_metadata(self) -> List[Dict]:
        """Load backup metadata from file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load backup metadata: {e}")
                
        return []
        
    def _save_backup_metadata(self) -> None:
        """Save backup metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.backup_metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save backup metadata: {e}")
            
    def _add_backup_entry(self, original_path: Path, backup_path: Path) -> None:
        """Add a new backup entry to metadata."""
        entry = {
            'original_path': str(original_path),
            'backup_path': str(backup_path),
            'created_at': datetime.now().isoformat(),
            'file_size': original_path.stat().st_size,
            'file_hash': self._calculate_file_hash(original_path)
        }
        
        self.backup_metadata.append(entry)
        self._save_backup_metadata()
        
    def _get_original_path(self, backup_path: Path) -> Optional[Path]:
        """Get original file path from backup metadata."""
        for entry in self.backup_metadata:
            if entry.get('backup_path') == str(backup_path):
                return Path(entry['original_path'])
        return None
        
    def _calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate MD5 hash of file content."""
        try:
            import hashlib
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return None
```

---

## Phase 2: Audio Processing (Week 3-4)

### Week 3: Audio File Detection and Validation

#### Day 1-2: Format Detection

**1. Implement `src/media/format_detector.py`**
```python
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
```

#### Day 3-4: Audio Metadata Handler

**1. Implement `src/media/audio_processor.py`**
```python
"""
Audio file processing for Media File Manager.

This module handles audio-specific operations including metadata
extraction, modification, and file processing.
"""

import mutagen
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Handles audio file processing and metadata operations.
    
    This class provides functionality to extract, modify, and write
    metadata for various audio formats.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize audio processor with configuration.
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.supported_formats = config.get('supported_formats', {}).get('audio', [])
        
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing extracted metadata
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                logger.warning(f"Could not read audio file: {file_path}")
                return {}
                
            metadata = {}
            
            # Extract common metadata fields
            metadata.update(self._extract_common_metadata(audio))
            
            # Extract format-specific metadata
            metadata.update(self._extract_format_metadata(audio, file_path))
            
            # Extract technical information
            metadata.update(self._extract_technical_info(audio, file_path))
            
            # Extract artwork if available
            artwork = self._extract_artwork(audio)
            if artwork:
                metadata['artwork'] = artwork
                
            logger.debug(f"Extracted metadata from {file_path}: {metadata}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}
            
    def update_metadata(self, file_path: Path, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata in audio file.
        
        Args:
            file_path: Path to the audio file
            metadata: Metadata to write
            
        Returns:
            True if metadata was updated successfully
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                logger.error(f"Could not read audio file for metadata update: {file_path}")
                return False
                
            # Update common metadata
            self._update_common_metadata(audio, metadata)
            
            # Update format-specific metadata
            self._update_format_metadata(audio, metadata)
            
            # Update artwork if provided
            if 'artwork' in metadata:
                self._update_artwork(audio, metadata['artwork'])
                
            # Save changes
            audio.save()
            
            logger.info(f"Successfully updated metadata for {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating metadata for {file_path}: {e}")
            return False
            
    def _extract_common_metadata(self, audio: mutagen.File) -> Dict[str, Any]:
        """Extract common metadata fields from audio file."""
        metadata = {}
        
        # Common ID3 tags
        common_tags = {
            'title': ['title', 'TIT2'],
            'artist': ['artist', 'TPE1'],
            'album': ['album', 'TALB'],
            'year': ['year', 'TDRC'],
            'genre': ['genre', 'TCON'],
            'track': ['track', 'TRCK'],
            'comment': ['comment', 'COMM'],
            'composer': ['composer', 'TCOM'],
            'lyrics': ['lyrics', 'USLT'],
        }
        
        for field, tag_names in common_tags.items():
            value = None
            for tag_name in tag_names:
                if hasattr(audio, 'tags') and audio.tags:
                    if tag_name in audio.tags:
                        value = str(audio.tags[tag_name][0])
                        break
                    elif hasattr(audio.tags, 'get') and audio.tags.get(tag_name):
                        value = str(audio.tags.get(tag_name)[0])
                        break
                        
            if value:
                metadata[field] = value
                
        return metadata
        
    def _extract_format_metadata(self, audio: mutagen.File, file_path: Path) -> Dict[str, Any]:
        """Extract format-specific metadata."""
        metadata = {}
        
        # MP3 specific
        if hasattr(audio, 'info') and hasattr(audio.info, 'bitrate'):
            metadata['bitrate'] = audio.info.bitrate
            
        # FLAC specific
        if hasattr(audio, 'info') and hasattr(audio.info, 'sample_rate'):
            metadata['sample_rate'] = audio.info.sample_rate
            metadata['channels'] = audio.info.channels
            metadata['bits_per_sample'] = audio.info.bits_per_sample
            
        # Vorbis comments (OGG, FLAC)
        if hasattr(audio, 'tags') and audio.tags:
            vorbis_tags = ['bpm', 'key', 'mood', 'language']
            for tag in vorbis_tags:
                if tag in audio.tags:
                    metadata[tag] = str(audio.tags[tag][0])
                    
        return metadata
        
    def _extract_technical_info(self, audio: mutagen.File, file_path: Path) -> Dict[str, Any]:
        """Extract technical information about the audio file."""
        info = {}
        
        if hasattr(audio, 'info'):
            if hasattr(audio.info, 'length'):
                info['duration'] = audio.info.length
            if hasattr(audio.info, 'bitrate'):
                info['bitrate'] = audio.info.bitrate
            if hasattr(audio.info, 'sample_rate'):
                info['sample_rate'] = audio.info.sample_rate
            if hasattr(audio.info, 'channels'):
                info['channels'] = audio.info.channels
                
        return info
        
    def _extract_artwork(self, audio: mutagen.File) -> Optional[Dict[str, Any]]:
        """Extract artwork from audio file."""
        try:
            if hasattr(audio, 'tags') and audio.tags:
                # Look for artwork in different tag formats
                artwork_keys = ['APIC:', 'APIC:cover', 'APIC:front', 'covr']
                
                for key in artwork_keys:
                    if key in audio.tags:
                        artwork_data = audio.tags[key]
                        if isinstance(artwork_data, list):
                            artwork_data = artwork_data[0]
                            
                        if hasattr(artwork_data, 'data'):
                            # Convert to PIL Image for processing
                            try:
                                image = Image.open(io.BytesIO(artwork_data.data))
                                return {
                                    'data': artwork_data.data,
                                    'format': image.format,
                                    'size': image.size,
                                    'mode': image.mode
                                }
                            except Exception as e:
                                logger.debug(f"Failed to process artwork: {e}")
                                
            return None
            
        except Exception as e:
            logger.debug(f"Error extracting artwork: {e}")
            return None
            
    def _update_common_metadata(self, audio: mutagen.File, metadata: Dict[str, Any]) -> None:
        """Update common metadata fields in audio file."""
        # Common ID3 tags mapping
        tag_mapping = {
            'title': 'TIT2',
            'artist': 'TPE1',
            'album': 'TALB',
            'year': 'TDRC',
            'genre': 'TCON',
            'track': 'TRCK',
            'comment': 'COMM',
            'composer': 'TCOM',
        }
        
        for field, tag_name in tag_mapping.items():
            if field in metadata and metadata[field]:
                if hasattr(audio, 'tags') and audio.tags:
                    audio.tags[tag_name] = str(metadata[field])
                    
    def _update_format_metadata(self, audio: mutagen.File, metadata: Dict[str, Any]) -> None:
        """Update format-specific metadata."""
        # Vorbis comments for OGG/FLAC
        if hasattr(audio, 'tags') and audio.tags:
            vorbis_fields = ['bpm', 'key', 'mood', 'language']
            for field in vorbis_fields:
                if field in metadata and metadata[field]:
                    audio.tags[field] = [str(metadata[field])]
                    
    def _update_artwork(self, audio: mutagen.File, artwork: Dict[str, Any]) -> None:
        """Update artwork in audio file."""
        try:
            if hasattr(audio, 'tags') and audio.tags:
                # Create APIC frame for ID3 tags
                from mutagen.id3 import APIC
                
                apic = APIC(
                    encoding=3,  # UTF-8
                    mime=artwork.get('format', 'image/jpeg'),
                    type=3,  # Front cover
                    desc='Cover',
                    data=artwork['data']
                )
                
                audio.tags['APIC:cover'] = apic
                
        except Exception as e:
            logger.error(f"Error updating artwork: {e}")
            
    def get_audio_properties(self, file_path: Path) -> Dict[str, Any]:
        """
        Get comprehensive audio properties.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio properties
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                return {}
                
            properties = {}
            
            if hasattr(audio, 'info'):
                info = audio.info
                
                # Basic properties
                if hasattr(info, 'length'):
                    properties['duration'] = info.length
                if hasattr(info, 'bitrate'):
                    properties['bitrate'] = info.bitrate
                if hasattr(info, 'sample_rate'):
                    properties['sample_rate'] = info.sample_rate
                if hasattr(info, 'channels'):
                    properties['channels'] = info.channels
                if hasattr(info, 'bits_per_sample'):
                    properties['bits_per_sample'] = info.bits_per_sample
                    
            return properties
            
        except Exception as e:
            logger.error(f"Error getting audio properties for {file_path}: {e}")
            return {}
```

#### Day 5-7: Audio File Renaming and Testing

**1. Implement audio-specific renaming logic in `src/core/file_renamer.py`**

**2. Create comprehensive tests for audio processing**

---

## Phase 3: Video Processing (Week 5-6)

### Week 5: Video File Detection and Validation

**1. Implement `src/media/video_processor.py`**

**2. Add video format support to format detector**

### Week 6: Video Metadata and Renaming

**1. Implement video metadata extraction and writing**

**2. Add video-specific renaming patterns**

---

## Phase 4: CLI Interface (Week 7)

### Week 7: Command-Line Interface

**1. Complete CLI implementation**

**2. Add progress indicators and user feedback**

**3. Implement help and usage information**

---

## Phase 5: Testing and Optimization (Week 8)

### Week 8: Final Testing and Documentation

**1. Comprehensive testing with real media files**

**2. Performance optimization**

**3. Documentation completion**

---

## Key Implementation Guidelines

### 1. Error Handling
- Use custom exception classes for different error types
- Implement comprehensive logging at all levels
- Provide user-friendly error messages
- Include rollback mechanisms for failed operations

### 2. Testing Strategy
- Unit tests for all core functions
- Integration tests for component interactions
- Mock external dependencies (file system, metadata libraries)
- Test with real media files in controlled environment

### 3. Performance Considerations
- Lazy loading of metadata and file properties
- Batch processing for multiple files
- Optional parallel processing for large libraries
- Efficient memory management for large files

### 4. Security Considerations
- Validate all file paths to prevent directory traversal
- Sanitize metadata values to prevent injection attacks
- Implement proper file permission handling
- Create secure backup mechanisms

### 5. Cross-Platform Compatibility
- Use `pathlib.Path` for file operations
- Handle different line endings and file systems
- Test on Windows, macOS, and Linux
- Use platform-agnostic libraries where possible

This roadmap provides a structured approach to implementing the Media File Manager project. Each phase builds upon the previous one, ensuring a solid foundation and maintainable codebase.
