"""
Network Scanner GUI Frame
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import threading
import logging
from datetime import datetime
import time

from core.wifi_scanner import WiFiScanner

logger = logging.getLogger(__name__)


class NetworkScannerFrame(ctk.CTkFrame):
    """Network scanner interface frame."""
    
    def __init__(self, parent, interface):
        super().__init__(parent)
        self.interface = interface
        self.scanner = WiFiScanner(interface)
        self.is_scanning = False
        self.scan_thread = None
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI elements
        self._create_header()
        self._create_network_list()
        self._create_details_panel()
        self._create_control_panel()
        
        logger.info("Network scanner frame initialized")
    
    def _create_header(self):
        """Create the header section."""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Network Scanner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Scan button
        self.scan_button = ctk.CTkButton(
            header_frame,
            text="Start Scan",
            command=self._toggle_scan,
            width=120
        )
        self.scan_button.pack(side="right", padx=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="Ready to scan",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right", padx=20)
    
    def _create_network_list(self):
        """Create the network list view."""
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview
        columns = ("SSID", "BSSID", "Channel", "Security", "Signal", "Quality")
        self.network_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="tree headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.network_tree.heading("#0", text="")
        self.network_tree.column("#0", width=30)
        
        self.network_tree.heading("SSID", text="Network Name")
        self.network_tree.column("SSID", width=200)
        
        self.network_tree.heading("BSSID", text="MAC Address")
        self.network_tree.column("BSSID", width=150)
        
        self.network_tree.heading("Channel", text="Ch")
        self.network_tree.column("Channel", width=50)
        
        self.network_tree.heading("Security", text="Security")
        self.network_tree.column("Security", width=100)
        
        self.network_tree.heading("Signal", text="Signal")
        self.network_tree.column("Signal", width=80)
        
        self.network_tree.heading("Quality", text="Quality")
        self.network_tree.column("Quality", width=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.network_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.network_tree.xview)
        self.network_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.network_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.network_tree.bind("<<TreeviewSelect>>", self._on_network_select)
        
        # Add tags for coloring
        self.network_tree.tag_configure("open", foreground="red")
        self.network_tree.tag_configure("wep", foreground="orange")
        self.network_tree.tag_configure("wpa", foreground="green")
        self.network_tree.tag_configure("wpa2", foreground="blue")
    
    def _create_details_panel(self):
        """Create the network details panel."""
        details_frame = ctk.CTkFrame(self)
        details_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Details text
        self.details_text = ctk.CTkTextbox(details_frame, height=150)
        self.details_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.details_text.configure(state="disabled")
    
    def _create_control_panel(self):
        """Create the control panel."""
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        # Channel selection
        channel_label = ctk.CTkLabel(control_frame, text="Channel:")
        channel_label.pack(side="left", padx=10)
        
        self.channel_var = tk.StringVar(value="All")
        self.channel_menu = ctk.CTkOptionMenu(
            control_frame,
            variable=self.channel_var,
            values=["All"] + [str(i) for i in range(1, 14)],
            width=80
        )
        self.channel_menu.pack(side="left", padx=5)
        
        # Export button
        self.export_button = ctk.CTkButton(
            control_frame,
            text="Export Results",
            command=self._export_results,
            width=120
        )
        self.export_button.pack(side="right", padx=10)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            control_frame,
            text="Clear",
            command=self._clear_results,
            width=80
        )
        self.clear_button.pack(side="right", padx=5)
    
    def _toggle_scan(self):
        """Toggle scanning on/off."""
        if not self.is_scanning:
            self._start_scan()
        else:
            self._stop_scan()
    
    def _start_scan(self):
        """Start network scanning."""
        self.is_scanning = True
        self.scan_button.configure(text="Stop Scan")
        self.status_label.configure(text="Scanning...")
        
        # Clear existing results
        self._clear_results()
        
        # Start scan thread
        self.scan_thread = threading.Thread(target=self._scan_worker, daemon=True)
        self.scan_thread.start()
        
        logger.info("Network scan started")
    
    def _stop_scan(self):
        """Stop network scanning."""
        self.is_scanning = False
        self.scan_button.configure(text="Start Scan")
        self.status_label.configure(text="Scan stopped")
        
        if self.scan_thread:
            self.scan_thread.join(timeout=1)
        
        logger.info("Network scan stopped")
    
    def _scan_worker(self):
        """Worker thread for network scanning."""
        try:
            while self.is_scanning:
                # Get channel to scan
                channel = self.channel_var.get()
                if channel == "All":
                    channels = list(range(1, 14))
                else:
                    channels = [int(channel)]
                
                # Scan networks
                for ch in channels:
                    if not self.is_scanning:
                        break
                    
                    networks = self.scanner.scan_networks(channel=ch)
                    
                    # Update UI in main thread
                    self.after(0, self._update_network_list, networks)
                    
                    # Small delay between channels
                    time.sleep(0.5)
                
                # Delay before next scan cycle
                time.sleep(2)
        
        except Exception as e:
            logger.error(f"Scan error: {e}")
            self.after(0, self._scan_error, str(e))
    
    def _update_network_list(self, networks):
        """Update the network list with scan results."""
        # Get existing items to avoid duplicates
        existing_bssids = set()
        for item in self.network_tree.get_children():
            values = self.network_tree.item(item)['values']
            if values:
                existing_bssids.add(values[1])  # BSSID is at index 1
        
        # Add new networks
        for network in networks:
            bssid = network.get('bssid', '')
            if bssid and bssid not in existing_bssids:
                ssid = network.get('ssid', '<Hidden>')
                channel = network.get('channel', 'N/A')
                security = network.get('security', 'Open')
                signal = network.get('signal', -100)
                quality = network.get('quality', 0)
                
                # Determine tag based on security
                tag = ""
                if security == "Open":
                    tag = "open"
                elif "WEP" in security:
                    tag = "wep"
                elif "WPA2" in security:
                    tag = "wpa2"
                elif "WPA" in security:
                    tag = "wpa"
                
                # Insert into tree
                self.network_tree.insert(
                    "",
                    "end",
                    values=(ssid, bssid, channel, security, f"{signal} dBm", f"{quality}%"),
                    tags=(tag,)
                )
        
        # Update status
        count = len(self.network_tree.get_children())
        self.status_label.configure(text=f"Found {count} networks")
    
    def _on_network_select(self, event):
        """Handle network selection."""
        selection = self.network_tree.selection()
        if selection:
            item = self.network_tree.item(selection[0])
            values = item['values']
            
            if values:
                # Display network details
                details = f"Network Details\n"
                details += f"{'='*50}\n"
                details += f"SSID: {values[0]}\n"
                details += f"BSSID: {values[1]}\n"
                details += f"Channel: {values[2]}\n"
                details += f"Security: {values[3]}\n"
                details += f"Signal Strength: {values[4]}\n"
                details += f"Quality: {values[5]}\n"
                details += f"\nLast Seen: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                # Calculate approximate distance
                try:
                    signal_dbm = int(values[4].replace(' dBm', ''))
                    from utils.network_utils import calculate_distance_from_rssi
                    distance = calculate_distance_from_rssi(signal_dbm)
                    if distance:
                        details += f"Approximate Distance: {distance} meters\n"
                except:
                    pass
                
                self.details_text.configure(state="normal")
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", details)
                self.details_text.configure(state="disabled")
    
    def _clear_results(self):
        """Clear scan results."""
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.configure(state="disabled")
        
        self.status_label.configure(text="Results cleared")
    
    def _export_results(self):
        """Export scan results to file."""
        # Get all networks from tree
        networks = []
        for item in self.network_tree.get_children():
            values = self.network_tree.item(item)['values']
            if values:
                networks.append({
                    'ssid': values[0],
                    'bssid': values[1],
                    'channel': values[2],
                    'security': values[3],
                    'signal': values[4],
                    'quality': values[5]
                })
        
        if not networks:
            messagebox.showwarning("No Data", "No networks to export")
            return
        
        # Save to file
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/scans/network_scan_{timestamp}.txt"
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                f.write(f"Network Scan Results - {datetime.now()}\n")
                f.write(f"Interface: {self.interface}\n")
                f.write(f"{'='*80}\n\n")
                
                for network in networks:
                    f.write(f"SSID: {network['ssid']}\n")
                    f.write(f"BSSID: {network['bssid']}\n")
                    f.write(f"Channel: {network['channel']}\n")
                    f.write(f"Security: {network['security']}\n")
                    f.write(f"Signal: {network['signal']}\n")
                    f.write(f"Quality: {network['quality']}\n")
                    f.write("-" * 40 + "\n")
            
            messagebox.showinfo("Export Complete", f"Results exported to:\n{filename}")
            logger.info(f"Scan results exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {e}")
            logger.error(f"Export error: {e}")
    
    def _scan_error(self, error_msg):
        """Handle scan errors."""
        self._stop_scan()
        messagebox.showerror("Scan Error", f"Scanning failed: {error_msg}")
    
    def cleanup(self):
        """Clean up resources."""
        self._stop_scan()
