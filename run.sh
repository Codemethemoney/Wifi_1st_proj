#!/bin/bash

# Wi-Fi Security Auditing Suite - One-Click Run Script
# Just run: ./run.sh

echo "╔═══════════════════════════════════════════════════════╗"
echo "║       Wi-Fi Security Auditing Suite Launcher          ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}This application requires admin privileges.${NC}"
    echo "Restarting with sudo..."
    echo ""
    exec sudo "$0" "$@"
fi

# Change to script directory
cd "$(dirname "$0")"

echo "📍 Working directory: $(pwd)"
echo ""

# Check Python installation
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Check and install dependencies
echo "📦 Checking dependencies..."

# Function to check if a Python package is installed
check_package() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Essential packages
PACKAGES=("customtkinter" "netifaces" "PIL")
MISSING_PACKAGES=()

for package in "${PACKAGES[@]}"; do
    if check_package "$package"; then
        echo -e "${GREEN}✅ $package is installed${NC}"
    else
        echo -e "${YELLOW}⚠️  $package is not installed${NC}"
        MISSING_PACKAGES+=("$package")
    fi
done

# Install missing packages
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo "📥 Installing missing packages..."
    
    # Install pip if not available
    if ! command -v pip3 &> /dev/null; then
        echo "Installing pip..."
        python3 -m ensurepip --default-pip
    fi
    
    # Install minimal requirements
    if [ -f "requirements-minimal.txt" ]; then
        echo "Installing from requirements-minimal.txt..."
        pip3 install -r requirements-minimal.txt --quiet
    else
        # Fallback to individual installs
        pip3 install customtkinter netifaces Pillow --quiet
    fi
    
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

echo ""
echo "🚨 System Requirements Check..."

# Check for airport utility
AIRPORT_PATH="/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
if [ -f "$AIRPORT_PATH" ]; then
    echo -e "${GREEN}✅ Airport utility found${NC}"
else
    echo -e "${YELLOW}⚠️  Airport utility not found - scanning may be limited${NC}"
fi

# Check if Wi-Fi is on
WIFI_STATUS=$(networksetup -getairportpower en0 2>/dev/null | grep "On")
if [ -n "$WIFI_STATUS" ]; then
    echo -e "${GREEN}✅ Wi-Fi is enabled${NC}"
else
    echo -e "${YELLOW}⚠️  Wi-Fi appears to be off - turning it on...${NC}"
    networksetup -setairportpower en0 on 2>/dev/null
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

# Create logs directory if it doesn't exist
mkdir -p logs/scans logs/captures

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ main.py not found!${NC}"
    echo "Make sure you're running this script from the project directory"
    exit 1
fi

# Launch the application
echo "🚀 Launching Wi-Fi Security Auditing Suite..."
echo ""
echo "📝 Tips:"
echo "  • Click 'Start Scan' to find Wi-Fi networks"
echo "  • Click on a network to see details"
echo "  • Use 'Export Results' to save scan data"
echo "  • Press Cmd+Q or close window to exit"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

# Run the application
python3 main.py 2>&1 | while IFS= read -r line; do
    # Filter out Tcl/Tk warnings that are harmless
    if [[ ! "$line" =~ "Tcl_FindHashEntry" ]] && [[ ! "$line" =~ "TKApplication" ]]; then
        echo "$line"
    fi
done

# Exit code
EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Application exited with error code: $EXIT_CODE${NC}"
    echo ""
    echo "Troubleshooting tips:"
    echo "1. Make sure you have the latest macOS updates"
    echo "2. Try running: pip3 install --upgrade customtkinter"
    echo "3. Check if Terminal has Location Services permission"
    echo "4. Report issues at: https://github.com/Codemethemoney/Wifi_1st_proj/issues"
else
    echo ""
    echo -e "${GREEN}✅ Application closed successfully${NC}"
fi

echo ""
echo "Thank you for using Wi-Fi Security Auditing Suite!"
