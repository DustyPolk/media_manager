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
