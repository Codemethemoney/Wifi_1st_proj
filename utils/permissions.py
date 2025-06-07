"""
Permission handling utilities for macOS
"""

import os
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)


def check_root_access():
    """Check if the application is running with root privileges."""
    return os.geteuid() == 0


def check_permissions():
    """Check if all required permissions are granted."""
    checks = {
        "Root access": check_root_access(),
        "Network interface access": check_network_access(),
        "Packet capture capability": check_pcap_capability()
    }
    
    all_passed = True
    for check, result in checks.items():
        if result:
            logger.info(f"✓ {check}: Passed")
        else:
            logger.error(f"✗ {check}: Failed")
            all_passed = False
    
    return all_passed


def check_network_access():
    """Check if we can access network interfaces."""
    try:
        result = subprocess.run(
            ["ifconfig", "-a"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to check network access: {e}")
        return False


def check_pcap_capability():
    """Check if packet capture is available."""
    try:
        # Check if tcpdump is available (it uses libpcap)
        result = subprocess.run(
            ["which", "tcpdump"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to check pcap capability: {e}")
        return False


def request_admin_privileges():
    """Request admin privileges using macOS authorization."""
    if check_root_access():
        return True
    
    logger.info("Requesting admin privileges...")
    
    # Re-run the script with sudo
    try:
        cmd = ["sudo", sys.executable] + sys.argv
        subprocess.run(cmd)
        return True
    except Exception as e:
        logger.error(f"Failed to obtain admin privileges: {e}")
        return False


def check_sip_status():
    """Check System Integrity Protection (SIP) status."""
    try:
        result = subprocess.run(
            ["csrutil", "status"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if "enabled" in result.stdout.lower():
            logger.warning("System Integrity Protection (SIP) is enabled")
            logger.warning("Some features may be limited")
            return False
        else:
            logger.info("System Integrity Protection (SIP) is disabled")
            return True
    except Exception as e:
        logger.error(f"Failed to check SIP status: {e}")
        return None


def check_wifi_adapter():
    """Check for available Wi-Fi adapters."""
    adapters = []
    
    try:
        # List all network interfaces
        result = subprocess.run(
            ["networksetup", "-listallhardwareports"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            current_port = None
            
            for line in lines:
                if line.startswith("Hardware Port:"):
                    current_port = line.split(":", 1)[1].strip()
                elif line.startswith("Device:") and current_port and "Wi-Fi" in current_port:
                    device = line.split(":", 1)[1].strip()
                    adapters.append({
                        "name": current_port,
                        "device": device
                    })
        
        # Check for USB Wi-Fi adapters
        usb_result = subprocess.run(
            ["system_profiler", "SPUSBDataType"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if "802.11" in usb_result.stdout or "wireless" in usb_result.stdout.lower():
            logger.info("External USB Wi-Fi adapter detected")
    
    except Exception as e:
        logger.error(f"Failed to check Wi-Fi adapters: {e}")
    
    return adapters


def enable_monitor_mode(interface):
    """Enable monitor mode on the specified interface."""
    if not check_root_access():
        logger.error("Root access required to enable monitor mode")
        return False
    
    try:
        # On macOS, we need to use airport utility
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        if os.path.exists(airport_path):
            # Disassociate from any network first
            subprocess.run([airport_path, "-z"], check=False)
            
            # Try to enable monitor mode
            result = subprocess.run(
                ["sudo", airport_path, interface, "sniff", "1"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                logger.info(f"Monitor mode enabled on {interface}")
                return True
            else:
                logger.error(f"Failed to enable monitor mode: {result.stderr}")
                return False
        else:
            logger.error("Airport utility not found")
            return False
            
    except Exception as e:
        logger.error(f"Error enabling monitor mode: {e}")
        return False


def disable_monitor_mode(interface):
    """Disable monitor mode on the specified interface."""
    try:
        # Simply bringing the interface down and up should restore normal mode
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=False)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=False)
        logger.info(f"Monitor mode disabled on {interface}")
        return True
    except Exception as e:
        logger.error(f"Error disabling monitor mode: {e}")
        return False
