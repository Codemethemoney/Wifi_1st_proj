"""
Network utility functions
"""

import os
import subprocess
import netifaces
import socket
import logging
import re

logger = logging.getLogger(__name__)


def get_network_interfaces():
    """Get list of available network interfaces."""
    interfaces = []
    
    try:
        # Get all interfaces
        all_interfaces = netifaces.interfaces()
        
        # Filter out loopback and other non-relevant interfaces
        for iface in all_interfaces:
            if iface.startswith('lo'):
                continue
            
            # Check if it's a valid network interface
            try:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs or netifaces.AF_INET6 in addrs:
                    interfaces.append(iface)
            except:
                continue
        
        # Sort interfaces to put common ones first
        def sort_key(iface):
            if iface.startswith('en'):
                return 0  # Ethernet/Wi-Fi
            elif iface.startswith('wlan'):
                return 1  # Wireless
            else:
                return 2  # Others
        
        interfaces.sort(key=sort_key)
        
    except Exception as e:
        logger.error(f"Error getting network interfaces: {e}")
        
        # Fallback method using ifconfig
        try:
            result = subprocess.run(
                ["ifconfig", "-a"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # Parse ifconfig output
                for line in result.stdout.split('\n'):
                    if line and not line.startswith('\t') and ':' in line:
                        iface = line.split(':')[0]
                        if not iface.startswith('lo'):
                            interfaces.append(iface)
        except:
            pass
    
    return interfaces


def get_interface_info(interface):
    """Get detailed information about a network interface."""
    info = {
        "name": interface,
        "mac": None,
        "ipv4": None,
        "ipv6": None,
        "status": "unknown",
        "type": "unknown"
    }
    
    try:
        addrs = netifaces.ifaddresses(interface)
        
        # Get MAC address
        if netifaces.AF_LINK in addrs:
            info["mac"] = addrs[netifaces.AF_LINK][0].get('addr')
        
        # Get IPv4 address
        if netifaces.AF_INET in addrs:
            info["ipv4"] = addrs[netifaces.AF_INET][0].get('addr')
        
        # Get IPv6 address
        if netifaces.AF_INET6 in addrs:
            info["ipv6"] = addrs[netifaces.AF_INET6][0].get('addr')
        
        # Check if interface is up
        result = subprocess.run(
            ["ifconfig", interface],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            if "status: active" in result.stdout:
                info["status"] = "active"
            elif "status: inactive" in result.stdout:
                info["status"] = "inactive"
            
            # Determine interface type
            if "Wi-Fi" in result.stdout or interface.startswith("en"):
                info["type"] = "wifi"
            elif "Ethernet" in result.stdout:
                info["type"] = "ethernet"
    
    except Exception as e:
        logger.error(f"Error getting interface info for {interface}: {e}")
    
    return info


def get_current_channel(interface):
    """Get the current channel of a Wi-Fi interface."""
    try:
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        if os.path.exists(airport_path):
            result = subprocess.run(
                [airport_path, "-I"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'channel:' in line:
                        # Extract channel number
                        match = re.search(r'channel:\s*(\d+)', line)
                        if match:
                            return int(match.group(1))
    except Exception as e:
        logger.error(f"Error getting current channel: {e}")
    
    return None


def set_channel(interface, channel):
    """Set the channel of a Wi-Fi interface."""
    try:
        # On macOS, changing channels requires the interface to be in monitor mode
        # and uses the airport utility
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        if os.path.exists(airport_path):
            result = subprocess.run(
                ["sudo", airport_path, interface, "channel", str(channel)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                logger.info(f"Set interface {interface} to channel {channel}")
                return True
            else:
                logger.error(f"Failed to set channel: {result.stderr}")
                return False
    except Exception as e:
        logger.error(f"Error setting channel: {e}")
    
    return False


def get_supported_channels(interface):
    """Get list of supported channels for a Wi-Fi interface."""
    channels = []
    
    try:
        # Get supported channels using airport utility
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        if os.path.exists(airport_path):
            result = subprocess.run(
                [airport_path, "-s"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # This gives us a scan, but we can infer supported channels
            # For now, return standard 2.4GHz and 5GHz channels
            channels = list(range(1, 14))  # 2.4GHz channels
            channels.extend([36, 40, 44, 48, 52, 56, 60, 64,  # 5GHz channels
                           100, 104, 108, 112, 116, 120, 124, 128,
                           132, 136, 140, 144, 149, 153, 157, 161, 165])
    
    except Exception as e:
        logger.error(f"Error getting supported channels: {e}")
        # Return default channels
        channels = list(range(1, 14))
    
    return channels


def get_signal_strength(bssid, interface):
    """Get signal strength for a specific BSSID."""
    try:
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        if os.path.exists(airport_path):
            result = subprocess.run(
                [airport_path, "-s"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if bssid.lower() in line.lower():
                        # Extract RSSI value
                        parts = line.split()
                        for part in parts:
                            if part.startswith('-') and part[1:].isdigit():
                                return int(part)
    
    except Exception as e:
        logger.error(f"Error getting signal strength: {e}")
    
    return None


def calculate_distance_from_rssi(rssi, frequency=2437):
    """
    Calculate approximate distance from RSSI value.
    Uses the log-distance path loss model.
    """
    # Path loss exponent (typically 2 for free space, 2.7-4.3 for obstructed)
    n = 3.0
    
    # Reference RSSI at 1 meter (typical value)
    rssi_ref = -30
    
    # Calculate distance
    try:
        distance = 10 ** ((rssi_ref - rssi) / (10 * n))
        return round(distance, 2)
    except:
        return None


def get_interface_mode(interface):
    """Get the current mode of the interface (managed/monitor)."""
    try:
        result = subprocess.run(
            ["ifconfig", interface],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # Check various indicators for monitor mode
            if "monitor" in result.stdout.lower():
                return "monitor"
            else:
                return "managed"
    
    except Exception as e:
        logger.error(f"Error getting interface mode: {e}")
    
    return "unknown"
