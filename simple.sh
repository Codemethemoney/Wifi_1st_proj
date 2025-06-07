#!/bin/bash

# Quick launcher for simple scanner
echo "🚀 Launching Simple Wi-Fi Scanner..."
echo "(This version works better with display issues)"
echo ""

if [ "$EUID" -ne 0 ]; then 
    exec sudo "$0" "$@"
fi

cd "$(dirname "$0")"
/usr/bin/python3 simple_scanner.py
