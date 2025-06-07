#!/bin/bash
# Quick network scan without GUI

echo "🔍 Quick Wi-Fi Network Scan"
echo "=========================="
echo ""

# Use airport utility directly
AIRPORT="/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

if [ -f "$AIRPORT" ]; then
    echo "Scanning for networks..."
    echo ""
    sudo $AIRPORT -s | head -20
    echo ""
    echo "Showing top 20 networks. For full GUI, run: ./run.sh"
else
    echo "Airport utility not found. Running Python scanner..."
    sudo python3 test_scanner.py
fi
