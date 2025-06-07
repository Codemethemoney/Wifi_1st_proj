"""
Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import threading
import logging
from datetime import datetime

from gui.network_scanner import NetworkScannerFrame
from gui.packet_monitor import PacketMonitorFrame
from gui.vulnerability_scanner import VulnerabilityScannerFrame

logger = logging.getLogger(__name__)

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow:
    """Main application window."""
    
    def __init__(self, interface):
        self.interface = interface
        self.root = ctk.CTk()
        self.root.title("Wi-Fi Security Auditing Suite")
        self.root.geometry("1200x800")
        
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
        
        logger.info("Main window initialized")
    
    def _create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="Wi-Fi Security\nAuditing Suite",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Interface label
        self.interface_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Interface: {self.interface}",
            font=ctk.CTkFont(size=12)
        )
        self.interface_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation buttons
        self.scanner_btn = ctk.CTkButton(
            self.sidebar,
            text="Network Scanner",
            command=self._show_network_scanner,
            width=180
        )
        self.scanner_btn.grid(row=2, column=0, padx=10, pady=10)
        
        self.monitor_btn = ctk.CTkButton(
            self.sidebar,
            text="Packet Monitor",
            command=self._show_packet_monitor,
            width=180
        )
        self.monitor_btn.grid(row=3, column=0, padx=10, pady=10)
        
        self.vuln_btn = ctk.CTkButton(
            self.sidebar,
            text="Vulnerability Scanner",
            command=self._show_vulnerability_scanner,
            width=180
        )
        self.vuln_btn.grid(row=4, column=0, padx=10, pady=10)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=self._show_settings,
            width=180,
            fg_color="gray"
        )
        self.settings_btn.grid(row=5, column=0, padx=10, pady=10)
        
        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=self._toggle_theme
        )
        self.theme_switch.grid(row=7, column=0, padx=20, pady=(10, 20))
        self.theme_switch.select()
    
    def _create_main_content(self):
        """Create the main content area."""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Content frames (initially hidden)
        self.network_scanner_frame = NetworkScannerFrame(self.main_frame, self.interface)
        self.packet_monitor_frame = PacketMonitorFrame(self.main_frame, self.interface)
        self.vulnerability_scanner_frame = VulnerabilityScannerFrame(self.main_frame, self.interface)
    
    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_bar = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.time_label.pack(side="right", padx=10)
        
        # Update time
        self._update_time()
    
    def _update_time(self):
        """Update the time display."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self._update_time)
    
    def _hide_all_frames(self):
        """Hide all content frames."""
        self.network_scanner_frame.grid_forget()
        self.packet_monitor_frame.grid_forget()
        self.vulnerability_scanner_frame.grid_forget()
    
    def _show_network_scanner(self):
        """Show the network scanner frame."""
        self._hide_all_frames()
        self.network_scanner_frame.grid(row=0, column=0, sticky="nsew")
        self.status_label.configure(text="Network Scanner Active")
        logger.info("Switched to Network Scanner")
    
    def _show_packet_monitor(self):
        """Show the packet monitor frame."""
        self._hide_all_frames()
        self.packet_monitor_frame.grid(row=0, column=0, sticky="nsew")
        self.status_label.configure(text="Packet Monitor Active")
        logger.info("Switched to Packet Monitor")
    
    def _show_vulnerability_scanner(self):
        """Show the vulnerability scanner frame."""
        self._hide_all_frames()
        self.vulnerability_scanner_frame.grid(row=0, column=0, sticky="nsew")
        self.status_label.configure(text="Vulnerability Scanner Active")
        logger.info("Switched to Vulnerability Scanner")
    
    def _show_settings(self):
        """Show settings dialog."""
        messagebox.showinfo("Settings", "Settings dialog not yet implemented")
    
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def _on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logger.info("Application closing...")
            # Clean up any running threads or processes
            self.network_scanner_frame.cleanup()
            self.packet_monitor_frame.cleanup()
            self.vulnerability_scanner_frame.cleanup()
            self.root.destroy()
    
    def run(self):
        """Run the main application loop."""
        logger.info("Starting main application loop")
        self.root.mainloop()
