"""
Command-line interface for Media File Manager.

This module provides a user-friendly command-line interface using Click
framework for processing media files and managing the application.
"""

import click
from pathlib import Path
from typing import Optional
import sys

from cli.commands import process_files, preview_changes, restore_backup, show_info
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
