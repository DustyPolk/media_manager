# Media File Manager - Project Structure Guide

## Complete Project Directory Structure

```
media_file_manager/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── metadata_handler.py
│   │   ├── file_renamer.py
│   │   └── validator.py
│   ├── media/
│   │   ├── __init__.py
│   │   ├── audio_processor.py
│   │   ├── video_processor.py
│   │   └── format_detector.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── file_utils.py
│   │   └── backup.py
│   └── cli/
│       ├── __init__.py
│       ├── commands.py
│       └── interface.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core/
│   │   ├── __init__.py
│   │   ├── test_file_processor.py
│   │   ├── test_metadata_handler.py
│   │   ├── test_file_renamer.py
│   │   └── test_validator.py
│   ├── test_media/
│   │   ├── __init__.py
│   │   ├── test_audio_processor.py
│   │   ├── test_video_processor.py
│   │   └── test_format_detector.py
│   ├── test_utils/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_logger.py
│   │   ├── test_file_utils.py
│   │   └── test_backup.py
│   └── test_cli/
│       ├── __init__.py
│       ├── test_commands.py
│       └── test_interface.py
├── config/
│   ├── default_config.yaml
│   └── user_config.yaml
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT.md
├── scripts/
│   ├── setup.py
│   ├── install_dependencies.py
│   └── run_tests.py
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── pyproject.toml
├── .gitignore
├── .flake8
├── .pylintrc
├── README.md
└── CHANGELOG.md
```

## Key Implementation Files

### 1. Entry Point (`src/main.py`)
```python
#!/usr/bin/env python3
"""
Media File Manager - Main Entry Point

This module serves as the main entry point for the Media File Manager application.
It handles command-line argument parsing and delegates to the appropriate modules.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from cli.interface import CLIInterface
from utils.config import ConfigManager
from utils.logger import setup_logging


def main() -> int:
    """Main entry point for the application."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Initialize CLI interface
        cli = CLIInterface(config)
        
        # Run CLI
        return cli.run()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### 2. Core File Processor (`src/core/file_processor.py`)
```python
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

from .validator import FileValidator
from .metadata_handler import MetadataHandler
from .file_renamer import FileRenamer
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
```

### 3. Configuration Manager (`src/utils/config.py`)
```python
"""
Configuration management for Media File Manager.

This module handles loading, validation, and access to configuration
settings from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dataclasses import dataclass, field


@dataclass
class ProcessingConfig:
    """Configuration for file processing."""
    backup_enabled: bool = True
    backup_directory: str = "./backups"
    parallel_processing: bool = False
    max_workers: int = 4
    update_metadata: bool = True
    create_backups: bool = True


@dataclass
class NamingConfig:
    """Configuration for file naming patterns."""
    audio_pattern: str = "{artist} - {title} ({year})"
    video_pattern: str = "{title} ({year}) - {quality}"
    replace_special_chars: bool = True
    case_standardization: str = "title"  # title, upper, lower


@dataclass
class MetadataConfig:
    """Configuration for metadata handling."""
    audio_required_fields: list = field(default_factory=lambda: ["artist", "title", "album", "year"])
    audio_optional_fields: list = field(default_factory=lambda: ["genre", "track", "bpm", "key"])
    video_required_fields: list = field(default_factory=lambda: ["title", "year"])
    video_optional_fields: list = field(default_factory=lambda: ["genre", "director", "cast", "description"])


@dataclass
class AppConfig:
    """Main application configuration."""
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    naming: NamingConfig = field(default_factory=NamingConfig)
    metadata: MetadataConfig = field(default_factory=MetadataConfig)
    supported_formats: list = field(default_factory=lambda: [
        # Audio formats
        ".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a",
        # Video formats
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"
    ])
    log_level: str = "INFO"
    log_file: Optional[str] = None


class ConfigManager:
    """Manages application configuration loading and access."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"
        self.config: Optional[AppConfig] = None
        
    def load_config(self) -> AppConfig:
        """Load configuration from files and environment."""
        if self.config is not None:
            return self.config
            
        # Load default configuration
        default_config = self._load_default_config()
        
        # Load user configuration (overrides defaults)
        user_config = self._load_user_config()
        
        # Merge configurations
        merged_config = self._merge_configs(default_config, user_config)
        
        # Apply environment variable overrides
        merged_config = self._apply_environment_overrides(merged_config)
        
        # Validate configuration
        self._validate_config(merged_config)
        
        self.config = merged_config
        return merged_config
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration from YAML file."""
        default_config_path = self.config_dir / "default_config.yaml"
        
        if default_config_path.exists():
            with open(default_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        else:
            return self._get_default_config_dict()
            
    def _load_user_config(self) -> Dict[str, Any]:
        """Load user configuration from YAML file."""
        user_config_path = self.config_dir / "user_config.yaml"
        
        if user_config_path.exists():
            with open(user_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        else:
            return {}
            
    def _get_default_config_dict(self) -> Dict[str, Any]:
        """Get default configuration as dictionary."""
        return {
            "processing": {
                "backup_enabled": True,
                "backup_directory": "./backups",
                "parallel_processing": False,
                "max_workers": 4,
                "update_metadata": True,
                "create_backups": True
            },
            "naming": {
                "audio_pattern": "{artist} - {title} ({year})",
                "video_pattern": "{title} ({year}) - {quality}",
                "replace_special_chars": True,
                "case_standardization": "title"
            },
            "metadata": {
                "audio_required_fields": ["artist", "title", "album", "year"],
                "audio_optional_fields": ["genre", "track", "bpm", "key"],
                "video_required_fields": ["title", "year"],
                "video_optional_fields": ["genre", "director", "cast", "description"]
            },
            "supported_formats": [
                ".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a",
                ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"
            ],
            "log_level": "INFO",
            "log_file": None
        }
        
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Merge user configuration with defaults."""
        merged = default.copy()
        
        def deep_merge(base: Dict, override: Dict):
            for key, value in override.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
                    
        deep_merge(merged, user)
        return merged
        
    def _apply_environment_overrides(self, config: Dict) -> Dict:
        """Apply environment variable overrides to configuration."""
        # Example: MEDIA_MANAGER_LOG_LEVEL=DEBUG
        env_prefix = "MEDIA_MANAGER_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                # Convert to appropriate type if possible
                if value.lower() in ('true', 'false'):
                    config[config_key] = value.lower() == 'true'
                elif value.isdigit():
                    config[config_key] = int(value)
                else:
                    config[config_key] = value
                    
        return config
        
    def _validate_config(self, config: Dict) -> None:
        """Validate configuration values."""
        # Add validation logic here
        pass
```

### 4. CLI Interface (`src/cli/interface.py`)
```python
"""
Command-line interface for Media File Manager.

This module provides a user-friendly command-line interface using Click
framework for processing media files and managing the application.
"""

import click
from pathlib import Path
from typing import Optional
import sys

from .commands import process_files, preview_changes, restore_backup, show_info
from utils.config import ConfigManager
from utils.logger import setup_logging


class CLIInterface:
    """Main CLI interface for the application."""
    
    def __init__(self, config: dict):
        """Initialize CLI interface with configuration."""
        self.config = config
        setup_logging(config.get('log_level', 'INFO'))
        
    def run(self) -> int:
        """Run the CLI application."""
        try:
            cli()
            return 0
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            return 1


@click.group()
@click.version_option(version="1.0.0")
@click.help_option()
def cli():
    """
    Media File Manager - Organize and tag your media files automatically.
    
    This tool helps you organize music and video files by renaming them
    according to consistent patterns and updating their metadata tags.
    """
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, path_type=Path))
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--backup/--no-backup', default=True, help='Create backups before processing')
@click.option('--parallel/--no-parallel', default=False, help='Enable parallel processing')
@click.option('--dry-run', is_flag=True, help='Preview changes without applying')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Minimal output')
def process(path: Path, config: Optional[str], backup: bool, parallel: bool, 
           dry_run: bool, verbose: bool, quiet: bool):
    """Process media files in the specified path."""
    if quiet:
        click.echo("Processing files...")
    else:
        click.echo(f"Processing media files in: {path}")
        
    # Load configuration
    config_manager = ConfigManager()
    app_config = config_manager.load_config()
    
    # Override config with CLI options
    if config:
        # Load custom config file
        pass
    if backup is not None:
        app_config['processing']['backup_enabled'] = backup
    if parallel is not None:
        app_config['processing']['parallel_processing'] = parallel
        
    # Process files
    if dry_run:
        preview_changes(path, app_config)
    else:
        process_files(path, app_config)


@cli.command()
@click.argument('path', type=click.Path(exists=True, path_type=Path))
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def preview(path: Path, config: Optional[str]):
    """Preview changes that would be made without applying them."""
    click.echo(f"Previewing changes for: {path}")
    
    config_manager = ConfigManager()
    app_config = config_manager.load_config()
    
    if config:
        # Load custom config file
        pass
        
    preview_changes(path, app_config)


@cli.command()
@click.argument('backup_path', type=click.Path(exists=True, path_type=Path))
@click.option('--force', '-f', is_flag=True, help='Force restoration without confirmation')
def restore(backup_path: Path, force: bool):
    """Restore files from a backup."""
    if not force:
        click.confirm(f"Are you sure you want to restore from {backup_path}?", abort=True)
        
    click.echo(f"Restoring from backup: {backup_path}")
    restore_backup(backup_path)


@cli.command()
def info():
    """Show application information and configuration."""
    show_info()


if __name__ == '__main__':
    cli()
```

## Configuration Files

### Default Configuration (`config/default_config.yaml`)
```yaml
# Media File Manager - Default Configuration

# File processing settings
processing:
  backup_enabled: true
  backup_directory: "./backups"
  parallel_processing: false
  max_workers: 4
  update_metadata: true
  create_backups: true

# File naming patterns
naming:
  audio_pattern: "{artist} - {title} ({year})"
  video_pattern: "{title} ({year}) - {quality}"
  replace_special_chars: true
  case_standardization: "title"  # title, upper, lower

# Metadata field requirements
metadata:
  audio:
    required_fields: ["artist", "title", "album", "year"]
    optional_fields: ["genre", "track", "bpm", "key"]
  video:
    required_fields: ["title", "year"]
    optional_fields: ["genre", "director", "cast", "description"]

# Supported file formats
supported_formats:
  audio: [".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a"]
  video: [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]

# Logging configuration
logging:
  level: "INFO"
  file: null
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Quality settings for video files
video_quality:
  hd: ["720p", "1080p", "1440p", "2160p"]
  sd: ["480p", "576p"]
  ultra_hd: ["4K", "8K"]
```

### User Configuration (`config/user_config.yaml`)
```yaml
# Media File Manager - User Configuration
# Override default settings here

# Custom naming patterns
naming:
  audio_pattern: "{artist} - {title} ({year}) [{bitrate}]"
  video_pattern: "{title} ({year}) [{quality}] [{codec}]"

# Custom metadata preferences
metadata:
  audio:
    required_fields: ["artist", "title", "album", "year", "genre"]
    optional_fields: ["track", "bpm", "key", "composer", "lyrics"]

# Processing preferences
processing:
  backup_directory: "~/media_backups"
  parallel_processing: true
  max_workers: 8

# Logging preferences
logging:
  level: "DEBUG"
  file: "~/media_manager.log"
```

## Dependencies

### Production Dependencies (`requirements.txt`)
```
# Audio processing
mutagen>=1.46.0
Pillow>=9.0.0

# Video processing
ffmpeg-python>=0.2.0
python-magic>=0.4.27

# Utilities
PyYAML>=6.0
click>=8.0.0
tqdm>=4.64.0
colorama>=0.4.5

# File handling
pathlib2>=2.3.7; python_version < "3.4"
```

### Development Dependencies (`requirements-dev.txt`)
```
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code quality
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
pylint>=2.15.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Development tools
pre-commit>=2.20.0
tox>=3.25.0
```

## Key Implementation Notes

### 1. Error Handling Strategy
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
