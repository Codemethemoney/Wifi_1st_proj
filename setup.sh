#!/bin/bash

# Wi-Fi Security Auditing Suite - Setup Script
# This script sets up necessary permissions and configurations for macOS

echo "Wi-Fi Security Auditing Suite - Setup Script"
echo "==========================================="

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run this script with sudo: sudo ./setup.sh"
    exit 1
fi

# Check macOS version
OS_VERSION=$(sw_vers -productVersion)
echo "Detected macOS version: $OS_VERSION"

# Check for Python 3.8+
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Detected Python version: $PYTHON_VERSION"

# Create logs directory if it doesn't exist
mkdir -p logs
chmod 755 logs

# Set up permissions for network interfaces
echo "Setting up network interface permissions..."

# Grant permissions for Wi-Fi scanning
echo "Granting permissions for Wi-Fi scanning..."

# Check for external Wi-Fi adapters
echo "Checking for external Wi-Fi adapters..."
system_profiler SPUSBDataType | grep -i "wi-fi\|wireless\|802.11" || echo "No external Wi-Fi adapter detected"

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install required system tools
echo "Installing required system tools..."
brew install libpcap tcpdump

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs/scans
mkdir -p logs/captures
mkdir -p data
mkdir -p config

# Set appropriate permissions
chmod -R 755 gui/
chmod -R 755 core/
chmod -R 755 utils/
chmod -R 777 logs/

# Create default configuration file
cat > config/default.conf << EOF
# Wi-Fi Security Auditing Suite Configuration
[general]
debug = false
log_level = INFO

[scanner]
default_interface = en0
scan_timeout = 30
channel_hop_interval = 0.5

[capture]
max_packet_size = 65536
capture_timeout = 300

[security]
enable_wpa_testing = false
enable_vulnerability_scan = true
EOF

echo ""
echo "Setup completed successfully!"
echo ""
echo "IMPORTANT NOTES:"
echo "1. This tool requires admin privileges to run"
echo "2. Always run with: sudo python3 main.py"
echo "3. For packet capture, you may need an external USB Wi-Fi adapter"
echo "4. Make sure to comply with all local laws and regulations"
echo ""
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
