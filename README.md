# Wi-Fi Security Auditing Suite

A comprehensive Python-based Wi-Fi security auditing tool for macOS with GUI interface.

## Features

- **Network Discovery**: Scan and discover available Wi-Fi networks
- **WPA/WPA2 Testing**: Security assessment for WPA/WPA2 protected networks
- **Network Monitoring**: Real-time packet capture and analysis
- **Vulnerability Assessment**: Identify common Wi-Fi security vulnerabilities
- **Signal Strength Analysis**: Monitor and visualize signal strength
- **Client Detection**: Identify connected devices on networks
- **Channel Analysis**: Analyze channel usage and interference

## Requirements

- macOS 10.15 or higher
- Python 3.8+
- Wi-Fi adapter with monitor mode support (external USB adapter recommended)
- Admin privileges for packet capture

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Grant necessary permissions:
   ```bash
   sudo chmod +x setup.sh
   ./setup.sh
   ```

## Usage

Run the application with admin privileges:
```bash
sudo python3 main.py
```

## Legal Notice

This tool is for authorized security testing only. Users must comply with all applicable laws and obtain proper authorization before testing any network.

## Project Structure

```
Wi-Fi exploits/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script for permissions
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── network_scanner.py # Network scanning interface
│   ├── packet_monitor.py  # Packet monitoring interface
│   └── vulnerability_scanner.py
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── wifi_scanner.py    # Wi-Fi network discovery
│   ├── packet_capture.py  # Packet capture engine
│   ├── wpa_tester.py      # WPA/WPA2 testing
│   └── vulnerability_checker.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── permissions.py     # Permission handling
│   ├── network_utils.py   # Network utilities
│   └── data_parser.py     # Data parsing utilities
└── logs/                  # Application logs
    └── .gitkeep
```
