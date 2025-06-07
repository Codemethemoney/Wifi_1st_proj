"""
Main Application Window - Fixed Version
Using standard tkinter to avoid rendering issues
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from datetime import datetime

from gui.network_scanner import NetworkScannerFrame
from gui.packet_monitor import PacketMonitorFrame
from gui.vulnerability_scanner import VulnerabilityScannerFrame

logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window - Fixed version using standard tkinter."""
    
    def __init__(self, interface):
        self.interface = interface
        self.root = tk.Tk()
        self.root.title("Wi-Fi Security Auditing Suite")
        self.root.geometry("1200x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#1e1e1e"
        self.sidebar_color = "#2d2d2d"
        self.button_color = "#0084ff"
        self.text_color = "#ffffff"
        
        # Configure root
        self.root.configure(bg=self.bg_color)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create UI elements
        self._create_sidebar()
        self._create_main_content()
        self._create_status_bar()
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Initialize with network scanner
        self._show_network_scanner()
        
        logger.info("Main window initialized (fixed version)")
    
    def _create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        self.sidebar = tk.Frame(self.root, width=200, bg=self.sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        logo_frame.pack(pady=20)
        
        tk.Label(logo_frame, text="Wi-Fi Security", 
                font=("Arial", 18, "bold"), 
                fg=self.text_color, bg=self.sidebar_color).pack()
        tk.Label(logo_frame, text="Auditing Suite", 
                font=("Arial", 18, "bold"), 
                fg=self.text_color, bg=self.sidebar_color).pack()
        
        # Interface label
        tk.Label(self.sidebar, text=f"Interface: {self.interface}",
                font=("Arial", 11), fg="#aaaaaa", 
                bg=self.sidebar_color).pack(pady=(0, 20))
        
        # Navigation buttons
        button_style = {
            "font": ("Arial", 12),
            "fg": self.text_color,
            "bg": self.button_color,
            "activebackground": "#0066cc",
            "activeforeground": self.text_color,
            "relief": "flat",
            "width": 18,
            "pady": 8
        }
        
        self.scanner_btn = tk.Button(self.sidebar, text="Network Scanner",
                                    command=self._show_network_scanner,
                                    **button_style)
        self.scanner_btn.pack(pady=5, padx=10)
        
        self.monitor_btn = tk.Button(self.sidebar, text="Packet Monitor",
                                    command=self._show_packet_monitor,
                                    **button_style)
        self.monitor_btn.pack(pady=5, padx=10)
        
        self.vuln_btn = tk.Button(self.sidebar, text="Vulnerability Scanner",
                                 command=self._show_vulnerability_scanner,
                                 **button_style)
        self.vuln_btn.pack(pady=5, padx=10)
        
        # Settings button
        settings_style = button_style.copy()
        settings_style["bg"] = "#666666"
        settings_style["activebackground"] = "#555555"
        
        self.settings_btn = tk.Button(self.sidebar, text="Settings",
                                     command=self._show_settings,
                                     **settings_style)
        self.settings_btn.pack(pady=5, padx=10)
        
        # Spacer
        tk.Frame(self.sidebar, bg=self.sidebar_color).pack(fill="both", expand=True)
        
        # Theme switch frame
        theme_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        theme_frame.pack(pady=20)
        
        self.dark_mode_var = tk.BooleanVar(value=True)
        self.theme_check = tk.Checkbutton(theme_frame, text="Dark Mode",
                                         variable=self.dark_mode_var,
                                         command=self._toggle_theme,
                                         font=("Arial", 11),
                                         fg=self.text_color,
                                         bg=self.sidebar_color,
                                         selectcolor=self.sidebar_color)
        self.theme_check.pack()
    
    def _create_main_content(self):
        """Create the main content area."""
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create a visible frame to show something is there
        content_bg = tk.Frame(self.main_frame, bg="#2a2a2a", relief="groove", bd=2)
        content_bg.grid(row=0, column=0, sticky="nsew")
        content_bg.grid_rowconfigure(0, weight=1)
        content_bg.grid_columnconfigure(0, weight=1)
        
        # For now, just show a label to confirm it's working
        self.content_label = tk.Label(content_bg, 
                                     text="Loading Network Scanner...",
                                     font=("Arial", 24),
                                     fg=self.text_color,
                                     bg="#2a2a2a")
        self.content_label.grid(row=0, column=0)
        
        # We'll replace the network scanner frames with simpler versions
        # For now, let's just get the UI visible
    
    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_bar = tk.Frame(self.root, height=30, bg="#333333")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, text="Ready",
                                    font=("Arial", 10),
                                    fg=self.text_color,
                                    bg="#333333")
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = tk.Label(self.status_bar, text="",
                                  font=("Arial", 10),
                                  fg=self.text_color,
                                  bg="#333333")
        self.time_label.pack(side="right", padx=10)
        
        # Update time
        self._update_time()
    
    def _update_time(self):
        """Update the time display."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self._update_time)
    
    def _show_network_scanner(self):
        """Show the network scanner."""
        self.content_label.configure(text="Network Scanner\n\nClick 'Start Scan' button here\n(Implementation coming)")
        self.status_label.configure(text="Network Scanner Active")
        
        # Clear content frame and add scanner button
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Create simple scanner interface
        scanner_frame = tk.Frame(self.main_frame, bg="#2a2a2a", relief="groove", bd=2)
        scanner_frame.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(scanner_frame, bg="#3a3a3a", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Network Scanner", 
                font=("Arial", 20, "bold"),
                fg=self.text_color, bg="#3a3a3a").pack(side="left", padx=20, pady=15)
        
        self.scan_btn = tk.Button(header, text="Start Scan",
                                 font=("Arial", 12),
                                 fg="white", bg="#4CAF50",
                                 command=self._toggle_scan,
                                 width=12)
        self.scan_btn.pack(side="right", padx=20, pady=15)
        
        # Network list
        list_frame = tk.Frame(scanner_frame, bg="#2a2a2a")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for networks
        columns = ("SSID", "BSSID", "Channel", "Signal", "Security")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=20)
        
        # Configure columns
        self.tree.heading("#0", text="#")
        self.tree.heading("SSID", text="Network Name")
        self.tree.heading("BSSID", text="MAC Address")
        self.tree.heading("Channel", text="Ch")
        self.tree.heading("Signal", text="Signal")
        self.tree.heading("Security", text="Security")
        
        self.tree.column("#0", width=40)
        self.tree.column("SSID", width=200)
        self.tree.column("BSSID", width=150)
        self.tree.column("Channel", width=50)
        self.tree.column("Signal", width=80)
        self.tree.column("Security", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add sample data to show it's working
        self.tree.insert("", "end", text="1", 
                        values=("Sample Network", "00:11:22:33:44:55", "6", "-50 dBm", "WPA2"))
        
        logger.info("Switched to Network Scanner")
    
    def _toggle_scan(self):
        """Toggle scan button."""
        if self.scan_btn["text"] == "Start Scan":
            self.scan_btn.configure(text="Stop Scan", bg="#f44336")
            self.status_label.configure(text="Scanning for networks...")
            # Add actual scanning logic here
        else:
            self.scan_btn.configure(text="Start Scan", bg="#4CAF50")
            self.status_label.configure(text="Scan stopped")
    
    def _show_packet_monitor(self):
        """Show the packet monitor."""
        self.content_label.configure(text="Packet Monitor\n\n(Coming Soon)")
        self.status_label.configure(text="Packet Monitor Active")
        logger.info("Switched to Packet Monitor")
    
    def _show_vulnerability_scanner(self):
        """Show the vulnerability scanner."""
        self.content_label.configure(text="Vulnerability Scanner\n\n(Coming Soon)")
        self.status_label.configure(text="Vulnerability Scanner Active")
        logger.info("Switched to Vulnerability Scanner")
    
    def _show_settings(self):
        """Show settings dialog."""
        messagebox.showinfo("Settings", "Settings dialog not yet implemented")
    
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.dark_mode_var.get():
            # Dark mode colors
            self.bg_color = "#1e1e1e"
            self.sidebar_color = "#2d2d2d"
        else:
            # Light mode colors
            self.bg_color = "#f0f0f0"
            self.sidebar_color = "#e0e0e0"
        
        # Update colors (simplified for now)
        self.root.configure(bg=self.bg_color)
        self.sidebar.configure(bg=self.sidebar_color)
    
    def _on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logger.info("Application closing...")
            self.root.destroy()
    
    def run(self):
        """Run the main application loop."""
        logger.info("Starting main application loop")
        self.root.mainloop()
