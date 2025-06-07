# Wi-Fi Security Auditing Suite

A comprehensive Python-based Wi-Fi security auditing tool for macOS with GUI interface.

## 🚀 Quick Start (One Command!)

Just run this single command:
```bash
./run.sh
```

That's it! The script will:
- ✅ Check for admin privileges (prompt for password if needed)
- ✅ Install any missing dependencies automatically
- ✅ Verify system requirements
- ✅ Launch the GUI application

## Features

- **Network Discovery**: Scan and discover available Wi-Fi networks
- **WPA/WPA2 Testing**: Security assessment for WPA/WPA2 protected networks
- **Network Monitoring**: Real-time packet capture and analysis
- **Vulnerability Assessment**: Identify common Wi-Fi security vulnerabilities
- **Signal Strength Analysis**: Monitor and visualize signal strength
- **Client Detection**: Identify connected devices on networks
- **Channel Analysis**: Analyze channel usage and interference

## Quick Commands

```bash
# Full GUI Application (recommended)
./run.sh

# Quick network scan (no GUI)
./quick-scan.sh

# Test if scanner works
sudo python3 test_scanner.py

# From anywhere on your system
cd ~/Desktop/"Wi-Fi exploits" && ./run.sh
```

## Requirements

- macOS 10.15 or higher
- Python 3.8+
- Wi-Fi adapter with monitor mode support (external USB adapter recommended)
- Admin privileges for packet capture

## Manual Installation

If you prefer manual setup:

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

### Easy Way (Recommended):
```bash
./run.sh
```

### Manual Way:
```bash
sudo python3 main.py
```

### Command Line Options:
```bash
# Use specific interface
sudo python3 main.py -i en0

# Enable debug mode
sudo python3 main.py -d

# Show version
python3 main.py -v
```

## Troubleshooting

### "Permission Denied" Error
The scanner requires admin privileges:
```bash
sudo ./run.sh
# OR
./run.sh  # (will auto-prompt for password)
```

### "Module Not Found" Error
Run the automatic installer:
```bash
./run.sh  # It will install missing modules automatically
```

### No Networks Found
1. Make sure Wi-Fi is ON
2. Enable Location Services for Terminal:
   - System Preferences → Security & Privacy → Privacy → Location Services
   - Enable for Terminal
3. Try the quick scan first:
   ```bash
   ./quick-scan.sh
   ```

## Legal Notice

This tool is for authorized security testing only. Users must:
- Only scan networks they own or have explicit permission to test
- Comply with all local laws and regulations
- Use responsibly and ethically

## Project Structure

```
Wi-Fi exploits/
├── run.sh                 # 🚀 One-click launcher (START HERE!)
├── quick-scan.sh         # Quick network scan
├── wifi-scan            # Alternative launcher
├── main.py              # Main application
├── test_scanner.py      # Test script
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── gui/                # GUI components
│   ├── main_window.py
│   ├── network_scanner.py
│   ├── packet_monitor.py
│   └── vulnerability_scanner.py
├── core/               # Core functionality
│   └── wifi_scanner.py
├── utils/              # Utilities
│   ├── permissions.py
│   └── network_utils.py
└── logs/               # Scan logs
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational purposes. Use at your own risk.

## Support

For issues or questions:
- Create an issue on GitHub
- Check existing issues for solutions
- Read the troubleshooting section

---

**Remember**: With great power comes great responsibility. Always use this tool ethically and legally!
