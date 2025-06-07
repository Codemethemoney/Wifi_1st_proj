#!/usr/bin/env python3
"""
Check if all dependencies are installed
"""

import subprocess
import sys

def check_dependencies():
    print("Checking Wi-Fi Scanner Dependencies")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"✓ Python version: {python_version}")
    
    # Check for required Python packages
    packages = {
        'tkinter': 'GUI framework',
        'customtkinter': 'Modern GUI widgets',
        'netifaces': 'Network interface detection',
        'logging': 'Logging (built-in)',
    }
    
    print("\nPython packages:")
    for package, description in packages.items():
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'customtkinter':
                import customtkinter
            elif package == 'netifaces':
                import netifaces
            elif package == 'logging':
                import logging
            print(f"✓ {package}: {description}")
        except ImportError:
            print(f"✗ {package}: NOT INSTALLED - {description}")
    
    # Check for system tools
    print("\nSystem tools:")
    tools = {
        'airport': '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport',
        'ifconfig': 'ifconfig',
        'networksetup': 'networksetup',
    }
    
    for tool, path in tools.items():
        try:
            result = subprocess.run(['which', path], capture_output=True, text=True)
            if result.returncode == 0 or (tool == 'airport' and subprocess.run(['ls', path], capture_output=True).returncode == 0):
                print(f"✓ {tool}: Found")
            else:
                print(f"✗ {tool}: NOT FOUND")
        except:
            print(f"✗ {tool}: ERROR checking")
    
    print("\n" + "=" * 50)
    print("To install missing Python packages, run:")
    print("pip3 install customtkinter netifaces")

if __name__ == "__main__":
    check_dependencies()
