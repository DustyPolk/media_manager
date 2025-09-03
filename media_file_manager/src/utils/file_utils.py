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
    invalid_chars = '<|>:"/\\|?*'
    
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
