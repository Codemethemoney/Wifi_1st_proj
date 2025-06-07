#!/bin/bash

# Fix tkinter installation for macOS
echo "🔧 Fixing tkinter installation..."
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check current Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Current Python version: $PYTHON_VERSION"
echo ""

# Method 1: Try installing python-tk via Homebrew
echo "Method 1: Installing python-tk via Homebrew..."
if command -v brew &> /dev/null; then
    brew install python-tk@3.13 2>/dev/null || brew install python-tk 2>/dev/null
    
    # Test if it worked
    if python3 -c "import tkinter" 2>/dev/null; then
        echo -e "${GREEN}✅ tkinter installed successfully!${NC}"
        echo ""
        echo "You can now run: ./run.sh"
        exit 0
    fi
fi

# Method 2: Use system Python which has tkinter
echo ""
echo "Method 2: Checking system Python..."
if /usr/bin/python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${GREEN}✅ System Python has tkinter!${NC}"
    echo ""
    echo "Creating launcher that uses system Python..."
    
    # Create a new launcher that uses system Python
    cat > run-system-python.sh << 'EOF'
#!/bin/bash
# Run with system Python that has tkinter

echo "🚀 Running with system Python..."

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    exec sudo "$0" "$@"
fi

cd "$(dirname "$0")"

# Install dependencies for system Python
/usr/bin/python3 -m pip install customtkinter netifaces Pillow --quiet 2>/dev/null

# Run the application
/usr/bin/python3 main.py
EOF

    chmod +x run-system-python.sh
    echo -e "${GREEN}✅ Created run-system-python.sh${NC}"
    echo ""
    echo "Run the application with:"
    echo "./run-system-python.sh"
    exit 0
fi

# Method 3: Install tkinter support
echo ""
echo "Method 3: Installing tkinter support..."
echo -e "${YELLOW}This may require reinstalling Python with tkinter support${NC}"
echo ""
echo "Options to fix this:"
echo ""
echo "1. Reinstall Python with tkinter:"
echo "   brew uninstall python@3.13"
echo "   brew install python-tk@3.13"
echo ""
echo "2. Use Python from python.org (includes tkinter):"
echo "   Download from: https://www.python.org/downloads/"
echo ""
echo "3. Use the system Python (recommended for GUI apps):"
echo "   We'll create a special launcher for this..."

# Create a fallback script that definitely works
cat > run-fallback.sh << 'EOF'
#!/bin/bash
# Fallback launcher that finds a Python with tkinter

echo "🔍 Finding Python with tkinter support..."

# List of Python executables to try
PYTHONS=(
    "/usr/bin/python3"
    "/usr/local/bin/python3"
    "/opt/homebrew/bin/python3"
    "python3"
    "python3.12"
    "python3.11"
    "python3.10"
    "python3.9"
)

WORKING_PYTHON=""

for py in "${PYTHONS[@]}"; do
    if command -v "$py" &> /dev/null; then
        if $py -c "import tkinter" 2>/dev/null; then
            WORKING_PYTHON="$py"
            echo "✅ Found working Python: $py"
            break
        fi
    fi
done

if [ -z "$WORKING_PYTHON" ]; then
    echo "❌ No Python installation with tkinter found!"
    echo ""
    echo "Please install Python from python.org:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    exec sudo "$0" "$@"
fi

cd "$(dirname "$0")"

# Install dependencies
echo "Installing dependencies..."
$WORKING_PYTHON -m pip install customtkinter netifaces Pillow --quiet

# Run the application
echo "Launching application..."
$WORKING_PYTHON main.py
EOF

chmod +x run-fallback.sh

echo ""
echo -e "${GREEN}✅ Created run-fallback.sh${NC}"
echo ""
echo "This script will find a Python with tkinter and use it."
echo ""
echo "Try running:"
echo "./run-fallback.sh"
