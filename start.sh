#!/bin/bash

# Quick fix: Run with system Python that has tkinter
echo "🚀 Wi-Fi Scanner - Quick Start"
echo "=============================="
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "📱 This app needs admin access to scan Wi-Fi networks."
    echo "   You'll be prompted for your password..."
    echo ""
    exec sudo "$0" "$@"
fi

cd "$(dirname "$0")"

# Quick dependency install using system Python
echo "📦 Setting up dependencies..."
/usr/bin/python3 -m pip install customtkinter netifaces Pillow --quiet 2>/dev/null || {
    # If pip fails, try without pip
    echo "   Installing with alternate method..."
    /usr/bin/python3 -m ensurepip --default-pip 2>/dev/null
    /usr/bin/python3 -m pip install customtkinter netifaces Pillow --quiet 2>/dev/null
}

echo "✅ Ready to go!"
echo ""
echo "🚀 Starting Wi-Fi Scanner..."
echo ""

# Run with system Python
/usr/bin/python3 main.py
