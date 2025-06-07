#!/usr/bin/env python3
"""
Test customtkinter theme fix
"""

import os
import sys

# Force light mode for testing
os.environ['APPEARANCE_MODE'] = 'light'

# Try importing and testing customtkinter
try:
    import customtkinter as ctk
    
    # Test window
    root = ctk.CTk()
    root.geometry("400x300")
    root.title("Theme Test")
    
    # Force update appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    label = ctk.CTkLabel(frame, text="If you can read this, it's working!", 
                         font=("Arial", 20))
    label.pack(pady=20)
    
    button = ctk.CTkButton(frame, text="Click Me!", 
                          command=lambda: print("Button clicked!"))
    button.pack(pady=10)
    
    root.mainloop()
    
except Exception as e:
    print(f"Error: {e}")
    print("\nFalling back to simple scanner...")
    os.system("python3 simple_scanner.py")
