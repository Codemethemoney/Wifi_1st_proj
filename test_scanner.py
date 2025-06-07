#!/usr/bin/env python3
"""
Quick test script to verify Wi-Fi scanning functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.wifi_scanner import WiFiScanner
from utils.network_utils import get_network_interfaces

def test_scan():
    print("Wi-Fi Scanner Test")
    print("=" * 50)
    
    # Get network interfaces
    interfaces = get_network_interfaces()
    print(f"Available interfaces: {interfaces}")
    
    if not interfaces:
        print("No network interfaces found!")
        return
    
    # Use first Wi-Fi interface (usually en0 on macOS)
    interface = interfaces[0]
    print(f"\nUsing interface: {interface}")
    
    # Create scanner
    scanner = WiFiScanner(interface)
    
    # Scan for networks
    print("\nScanning for Wi-Fi networks...")
    networks = scanner.scan_networks()
    
    if networks:
        print(f"\nFound {len(networks)} networks:\n")
        for network in networks:
            ssid = network.get('ssid', '<Hidden>')
            bssid = network.get('bssid', 'Unknown')
            channel = network.get('channel', 'N/A')
            signal = network.get('signal', -100)
            security = network.get('security', 'Unknown')
            quality = network.get('quality', 0)
            
            print(f"SSID: {ssid:30} | Channel: {channel:3} | Signal: {signal:4} dBm | Security: {security}")
    else:
        print("No networks found. Make sure:")
        print("1. Wi-Fi is enabled")
        print("2. You're running with sudo")
        print("3. Location services are enabled for Terminal")

if __name__ == "__main__":
    test_scan()
