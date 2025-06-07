"""
Packet Monitor GUI Frame
"""

import tkinter as tk
import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)


class PacketMonitorFrame(ctk.CTkFrame):
    """Packet monitoring interface frame."""
    
    def __init__(self, parent, interface):
        super().__init__(parent)
        self.interface = interface
        
        # Create placeholder UI
        label = ctk.CTkLabel(
            self,
            text="Packet Monitor\n\nComing Soon...",
            font=ctk.CTkFont(size=24)
        )
        label.pack(expand=True)
        
        logger.info("Packet monitor frame initialized (placeholder)")
    
    def cleanup(self):
        """Clean up resources."""
        pass
