#!/usr/bin/env python3
"""
Media File Manager - Main Entry Point

This module serves as the main entry point for the Media File Manager application.
It handles command-line argument parsing and delegates to the appropriate modules.
"""

import sys
import logging
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
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
