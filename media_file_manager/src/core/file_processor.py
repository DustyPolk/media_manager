"""
Core file processing module for Media File Manager.

This module orchestrates the entire file processing workflow, including
validation, backup creation, metadata extraction, file renaming, and
metadata updating.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from core.validator import FileValidator
from core.metadata_handler import MetadataHandler
from core.file_renamer import FileRenamer
from utils.backup import BackupManager
from utils.logger import get_logger


@dataclass
class ProcessingResult:
    """Result of file processing operation."""
    success: bool
    original_path: Path
    new_path: Optional[Path]
    metadata: Dict
    errors: List[str]
    warnings: List[str]


class FileProcessor:
    """
    Main file processor that orchestrates the entire workflow.
    
    This class coordinates all aspects of file processing including
    validation, backup, metadata handling, and file renaming.
    """
    
    def __init__(self, config: Dict):
        """Initialize the file processor with configuration."""
        self.config = config
        self.logger = get_logger(__name__)
        self.validator = FileValidator(config)
        self.metadata_handler = MetadataHandler(config)
        self.file_renamer = FileRenamer(config)
        self.backup_manager = BackupManager(config)
        
    def process_file(self, file_path: Path) -> ProcessingResult:
        """
        Process a single media file.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            ProcessingResult containing the outcome of processing
        """
        self.logger.info(f"Processing file: {file_path}")
        
        # Initialize result
        result = ProcessingResult(
            success=False,
            original_path=file_path,
            new_path=None,
            metadata={},
            errors=[],
            warnings=[]
        )
        
        try:
            # Step 1: Validate file
            if not self.validator.validate_file(file_path):
                result.errors.append("File validation failed")
                return result
                
            # Step 2: Create backup
            if self.config.get('backup_enabled', True):
                backup_path = self.backup_manager.create_backup(file_path)
                if not backup_path:
                    result.warnings.append("Failed to create backup")
                    
            # Step 3: Extract metadata
            metadata = self.metadata_handler.extract_metadata(file_path)
            result.metadata = metadata
            
            # Step 4: Generate new filename
            new_filename = self.file_renamer.generate_filename(file_path, metadata)
            if not new_filename:
                result.errors.append("Failed to generate new filename")
                return result
                
            # Step 5: Rename file
            new_path = self.file_renamer.rename_file(file_path, new_filename)
            if not new_path:
                result.errors.append("Failed to rename file")
                return result
                
            result.new_path = new_path
            
            # Step 6: Update metadata
            if self.config.get('update_metadata', True):
                success = self.metadata_handler.update_metadata(new_path, metadata)
                if not success:
                    result.warnings.append("Failed to update metadata")
                    
            # Step 7: Validate final result
            if self.validator.validate_file(new_path):
                result.success = True
                self.logger.info(f"Successfully processed: {new_path}")
            else:
                result.errors.append("Final validation failed")
                
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            result.errors.append(str(e))
            
        return result
        
    def process_directory(self, directory_path: Path) -> List[ProcessingResult]:
        """
        Process all media files in a directory.
        
        Args:
            directory_path: Path to directory containing media files
            
        Returns:
            List of ProcessingResult objects for each processed file
        """
        self.logger.info(f"Processing directory: {directory_path}")
        
        results = []
        media_files = self._find_media_files(directory_path)
        
        for file_path in media_files:
            result = self.process_file(file_path)
            results.append(result)
            
        return results
        
    def _find_media_files(self, directory_path: Path) -> List[Path]:
        """Find all media files in the given directory."""
        supported_formats = self.config.get('supported_formats', [])
        media_files = []
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and self._is_media_file(file_path, supported_formats):
                media_files.append(file_path)
                
        return media_files
        
    def _is_media_file(self, file_path: Path, supported_formats: List[str]) -> bool:
        """Check if a file is a supported media format."""
        return file_path.suffix.lower() in supported_formats
