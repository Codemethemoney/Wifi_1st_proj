#!/bin/bash

# Fixed GUI Launcher
echo "🚀 Launching Wi-Fi Scanner (Fixed GUI)..."
echo ""

if [ "$EUID" -ne 0 ]; then 
    exec sudo "$0" "$@"
fi

cd "$(dirname "$0")"
/usr/bin/python3 main_fixed.py
