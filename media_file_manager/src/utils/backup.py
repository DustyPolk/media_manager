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
