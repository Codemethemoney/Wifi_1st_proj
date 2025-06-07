#!/usr/bin/env python3
"""
Wi-Fi Security Auditing Suite
Main Application Entry Point
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from utils.permissions import check_permissions, check_root_access
from utils.network_utils import get_network_interfaces

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Wi-Fi Security Auditing Suite for macOS'
    )
    parser.add_argument(
        '--interface', '-i',
        type=str,
        help='Network interface to use (default: auto-detect)'
    )
    parser.add_argument(
        '--headless', '-H',
        action='store_true',
        help='Run in headless mode (no GUI)'
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Wi-Fi Security Auditing Suite v1.0.0'
    )
    
    return parser.parse_args()


def initialize_application():
    """Initialize the application and check requirements."""
    logger.info("Starting Wi-Fi Security Auditing Suite...")
    
    # Check for root access
    if not check_root_access():
        logger.error("This application requires root privileges.")
        logger.error("Please run with: sudo python3 main.py")
        sys.exit(1)
    
    # Check system permissions
    if not check_permissions():
        logger.error("Missing required system permissions.")
        logger.error("Please run setup.sh first: sudo ./setup.sh")
        sys.exit(1)
    
    # Get available network interfaces
    interfaces = get_network_interfaces()
    if not interfaces:
        logger.error("No network interfaces found.")
        sys.exit(1)
    
    logger.info(f"Found {len(interfaces)} network interface(s)")
    for iface in interfaces:
        logger.info(f"  - {iface}")
    
    return interfaces


def main():
    """Main application entry point."""
    args = parse_arguments()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Initialize application
    try:
        interfaces = initialize_application()
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        sys.exit(1)
    
    # Select interface
    if args.interface:
        if args.interface not in interfaces:
            logger.error(f"Interface '{args.interface}' not found")
            logger.error(f"Available interfaces: {', '.join(interfaces)}")
            sys.exit(1)
        selected_interface = args.interface
    else:
        # Auto-select first available interface
        selected_interface = interfaces[0]
    
    logger.info(f"Using interface: {selected_interface}")
    
    # Run application
    if args.headless:
        logger.info("Running in headless mode...")
        # TODO: Implement headless mode functionality
        logger.warning("Headless mode not yet implemented")
    else:
        logger.info("Starting GUI...")
        try:
            app = MainWindow(selected_interface)
            app.run()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            sys.exit(1)
    
    logger.info("Application terminated")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
