#!/usr/bin/env python3
"""
Wi-Fi Scanner - Simple Version
This version uses standard tkinter to avoid theme issues
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
from datetime import datetime

class SimpleWiFiScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wi-Fi Scanner - Simple Mode")
        self.root.geometry("900x600")
        
        # Variables
        self.is_scanning = False
        self.networks = {}
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2b2b2b', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(header_frame, text="Wi-Fi Network Scanner", 
                        font=('Arial', 24, 'bold'), fg='white', bg='#2b2b2b')
        title.pack(side='left', padx=20, pady=10)
        
        # Scan Button
        self.scan_btn = tk.Button(header_frame, text="Start Scan", 
                                 command=self.toggle_scan, font=('Arial', 12),
                                 bg='#4CAF50', fg='white', padx=20)
        self.scan_btn.pack(side='right', padx=20, pady=15)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Network List
        list_frame = tk.LabelFrame(main_frame, text="Detected Networks", 
                                  font=('Arial', 12, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ('SSID', 'BSSID', 'Channel', 'Signal', 'Security')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        # Column headings
        self.tree.heading('#0', text='#')
        self.tree.heading('SSID', text='Network Name')
        self.tree.heading('BSSID', text='MAC Address')
        self.tree.heading('Channel', text='Ch')
        self.tree.heading('Signal', text='Signal')
        self.tree.heading('Security', text='Security')
        
        # Column widths
        self.tree.column('#0', width=40)
        self.tree.column('SSID', width=200)
        self.tree.column('BSSID', width=150)
        self.tree.column('Channel', width=50)
        self.tree.column('Signal', width=80)
        self.tree.column('Security', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to scan")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bd=1, relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
    def toggle_scan(self):
        if not self.is_scanning:
            self.start_scan()
        else:
            self.stop_scan()
            
    def start_scan(self):
        self.is_scanning = True
        self.scan_btn.config(text="Stop Scan", bg='#f44336')
        self.status_var.set("Scanning for networks...")
        self.tree.delete(*self.tree.get_children())
        
        # Start scan thread
        self.scan_thread = threading.Thread(target=self.scan_worker, daemon=True)
        self.scan_thread.start()
        
    def stop_scan(self):
        self.is_scanning = False
        self.scan_btn.config(text="Start Scan", bg='#4CAF50')
        self.status_var.set("Scan stopped")
        
    def scan_worker(self):
        """Background scanning thread"""
        airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        count = 0
        
        while self.is_scanning:
            try:
                # Run airport scan
                result = subprocess.run([airport, "-s"], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Parse results
                    lines = result.stdout.strip().split('\n')
                    
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 7:
                                ssid = parts[0] if parts[0] != '(null)' else '<Hidden>'
                                bssid = parts[1]
                                signal = parts[2]
                                channel = parts[3].split(',')[0]
                                security = ' '.join(parts[6:]) if len(parts) > 6 else 'Open'
                                
                                # Update in main thread
                                self.root.after(0, self.update_network, 
                                              ssid, bssid, channel, signal, security)
                    
                    count = len(self.networks)
                    self.root.after(0, lambda: self.status_var.set(f"Found {count} networks"))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            
            # Wait before next scan
            time.sleep(3)
    
    def update_network(self, ssid, bssid, channel, signal, security):
        """Update network in the list"""
        # Check if already exists
        if bssid not in self.networks:
            # Add to tree
            count = len(self.networks) + 1
            
            # Determine color based on security
            tags = ()
            if security == 'Open':
                tags = ('open',)
            elif 'WEP' in security:
                tags = ('wep',)
            elif 'WPA2' in security:
                tags = ('wpa2',)
            elif 'WPA' in security:
                tags = ('wpa',)
            
            self.tree.insert('', 'end', values=(ssid, bssid, channel, 
                                               f"{signal} dBm", security),
                           text=str(count), tags=tags)
            
            # Configure tag colors
            self.tree.tag_configure('open', foreground='red')
            self.tree.tag_configure('wep', foreground='orange')
            self.tree.tag_configure('wpa', foreground='green')
            self.tree.tag_configure('wpa2', foreground='blue')
            
            # Store in dict
            self.networks[bssid] = {
                'ssid': ssid,
                'channel': channel,
                'signal': signal,
                'security': security
            }
    
    def on_select(self, event):
        """Handle network selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            if values:
                # Show details in a popup
                details = f"Network Details\n\n"
                details += f"SSID: {values[0]}\n"
                details += f"BSSID: {values[1]}\n"
                details += f"Channel: {values[2]}\n"
                details += f"Signal: {values[3]}\n"
                details += f"Security: {values[4]}\n\n"
                
                # Calculate approximate distance
                try:
                    signal_dbm = int(values[3].replace(' dBm', ''))
                    distance = 10 ** ((30 - abs(signal_dbm)) / (10 * 3.0))
                    details += f"Approx. Distance: {distance:.1f} meters"
                except:
                    pass
                
                messagebox.showinfo("Network Information", details)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Simple Wi-Fi Scanner...")
    print("This version uses standard tkinter to avoid display issues.")
    print("")
    
    app = SimpleWiFiScanner()
    app.run()
