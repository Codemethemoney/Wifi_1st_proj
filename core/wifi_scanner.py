"""
Wi-Fi Scanner Core Module
"""

import os
import subprocess
import re
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class WiFiScanner:
    """Core Wi-Fi scanning functionality."""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        
        # Check if airport utility exists
        if not os.path.exists(self.airport_path):
            logger.warning("Airport utility not found. Some features may be limited.")
            self.airport_path = None
    
    def scan_networks(self, channel: Optional[int] = None) -> List[Dict]:
        """
        Scan for available Wi-Fi networks.
        
        Args:
            channel: Specific channel to scan (None for all channels)
            
        Returns:
            List of network dictionaries
        """
        networks = []
        
        try:
            if self.airport_path:
                # Use airport utility for scanning
                networks = self._scan_with_airport()
            else:
                # Fallback to system profiler
                networks = self._scan_with_system_profiler()
            
            # Filter by channel if specified
            if channel:
                networks = [n for n in networks if n.get('channel') == channel]
            
            # Calculate quality scores
            for network in networks:
                network['quality'] = self._calculate_quality(network.get('signal', -100))
            
        except Exception as e:
            logger.error(f"Error scanning networks: {e}")
        
        return networks
    
    def _scan_with_airport(self) -> List[Dict]:
        """Scan networks using airport utility."""
        networks = []
        
        try:
            # Run airport scan
            result = subprocess.run(
                [self.airport_path, "-s"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # Parse output
                lines = result.stdout.strip().split('\n')
                
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 7:
                            network = {
                                'ssid': parts[0] if parts[0] != '(null)' else '<Hidden>',
                                'bssid': parts[1],
                                'signal': int(parts[2]),
                                'channel': self._parse_channel(parts[3]),
                                'ht': parts[4],
                                'cc': parts[5],
                                'security': ' '.join(parts[6:]) if len(parts) > 6 else 'Open',
                                'timestamp': datetime.now()
                            }
                            networks.append(network)
            else:
                logger.error(f"Airport scan failed: {result.stderr}")
        
        except Exception as e:
            logger.error(f"Error in airport scan: {e}")
        
        return networks
    
    def _scan_with_system_profiler(self) -> List[Dict]:
        """Fallback scanning method using system profiler."""
        networks = []
        
        try:
            # Get current network info
            result = subprocess.run(
                ["system_profiler", "SPAirPortDataType"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # Parse basic network info
                # This is limited compared to airport utility
                current_network = self._parse_current_network(result.stdout)
                if current_network:
                    networks.append(current_network)
        
        except Exception as e:
            logger.error(f"Error in system profiler scan: {e}")
        
        return networks
    
    def _parse_channel(self, channel_str: str) -> int:
        """Parse channel string to integer."""
        try:
            # Remove any frequency info (e.g., "6,+1")
            channel = channel_str.split(',')[0]
            return int(channel)
        except:
            return 0
    
    def _parse_current_network(self, profiler_output: str) -> Optional[Dict]:
        """Parse current network from system profiler output."""
        network = None
        
        try:
            lines = profiler_output.split('\n')
            current_ssid = None
            current_bssid = None
            current_channel = None
            
            for line in lines:
                line = line.strip()
                
                if "Current Network Information:" in line:
                    # Start of current network section
                    continue
                
                match = re.match(r'(\w+):\s*(.+)', line)
                if match:
                    key, value = match.groups()
                    
                    if key == "SSID":
                        current_ssid = value
                    elif key == "BSSID":
                        current_bssid = value
                    elif key == "Channel":
                        try:
                            current_channel = int(value.split()[0])
                        except:
                            pass
            
            if current_ssid and current_bssid:
                network = {
                    'ssid': current_ssid,
                    'bssid': current_bssid,
                    'channel': current_channel or 0,
                    'signal': -50,  # Estimate
                    'security': 'Unknown',
                    'timestamp': datetime.now()
                }
        
        except Exception as e:
            logger.error(f"Error parsing current network: {e}")
        
        return network
    
    def _calculate_quality(self, signal: int) -> int:
        """
        Calculate signal quality percentage from RSSI.
        
        Args:
            signal: RSSI value in dBm
            
        Returns:
            Quality percentage (0-100)
        """
        # Typical RSSI ranges:
        # -30 dBm = Excellent (100%)
        # -67 dBm = Very Good (75%)
        # -70 dBm = Good (50%)
        # -80 dBm = Fair (25%)
        # -90 dBm = Poor (0%)
        
        if signal >= -30:
            return 100
        elif signal >= -67:
            return int(75 + (signal + 67) * 25 / 37)
        elif signal >= -70:
            return int(50 + (signal + 70) * 25 / 3)
        elif signal >= -80:
            return int(25 + (signal + 80) * 25 / 10)
        elif signal >= -90:
            return int((signal + 90) * 25 / 10)
        else:
            return 0
    
    def get_network_details(self, bssid: str) -> Optional[Dict]:
        """Get detailed information about a specific network."""
        networks = self.scan_networks()
        
        for network in networks:
            if network.get('bssid') == bssid:
                # Add additional details
                network['vendor'] = self._lookup_vendor(bssid)
                network['frequency'] = self._channel_to_frequency(network.get('channel', 0))
                return network
        
        return None
    
    def _lookup_vendor(self, mac_address: str) -> str:
        """Look up vendor from MAC address OUI."""
        # This would normally use an OUI database
        # For now, return a placeholder
        oui = mac_address[:8].upper()
        
        # Common vendor OUIs
        vendors = {
            "00:1B:63": "Apple",
            "00:1E:52": "Apple",
            "00:1F:F3": "Apple",
            "00:23:12": "Apple",
            "00:25:00": "Apple",
            "00:26:08": "Apple",
            "3C:5A:B4": "Google",
            "F4:F5:D8": "Google",
            "00:1A:11": "Google",
            "94:B4:0F": "Aruba Networks",
            "00:0B:86": "Aruba Networks",
            "00:24:6C": "Aruba Networks",
        }
        
        return vendors.get(oui, "Unknown")
    
    def _channel_to_frequency(self, channel: int) -> int:
        """Convert channel number to frequency in MHz."""
        if 1 <= channel <= 14:
            # 2.4 GHz band
            if channel == 14:
                return 2484
            else:
                return 2412 + (channel - 1) * 5
        elif 36 <= channel <= 165:
            # 5 GHz band
            return 5180 + (channel - 36) * 5
        else:
            return 0
    
    def start_continuous_scan(self, callback, interval: int = 5):
        """
        Start continuous scanning with callback.
        
        Args:
            callback: Function to call with scan results
            interval: Seconds between scans
        """
        self._scanning = True
        
        while self._scanning:
            networks = self.scan_networks()
            callback(networks)
            time.sleep(interval)
    
    def stop_continuous_scan(self):
        """Stop continuous scanning."""
        self._scanning = False
    
    def export_scan_results(self, networks: List[Dict], filename: str):
        """Export scan results to file."""
        try:
            with open(filename, 'w') as f:
                f.write(f"Wi-Fi Scan Results\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Interface: {self.interface}\n")
                f.write("=" * 80 + "\n\n")
                
                for network in networks:
                    f.write(f"SSID: {network.get('ssid', 'N/A')}\n")
                    f.write(f"BSSID: {network.get('bssid', 'N/A')}\n")
                    f.write(f"Channel: {network.get('channel', 'N/A')}\n")
                    f.write(f"Signal: {network.get('signal', 'N/A')} dBm\n")
                    f.write(f"Quality: {network.get('quality', 'N/A')}%\n")
                    f.write(f"Security: {network.get('security', 'N/A')}\n")
                    f.write(f"Vendor: {network.get('vendor', 'N/A')}\n")
                    f.write("-" * 40 + "\n")
            
            logger.info(f"Scan results exported to {filename}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to export scan results: {e}")
            return False
