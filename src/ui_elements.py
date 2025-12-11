"""
AFK Auto-Help Module: UI Helper Elements

This module contains reusable UI components and helper functions for
building the Tkinter GUI. This is an optional module for cleaner code
organization.

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 1 (Core GUI Framework)
and later phases as needed.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple


# TODO: Phase 7 - Add visual design improvements


def create_status_bar(parent) -> ttk.Label:
    """
    Create a status bar widget for displaying real-time information.
    
    Args:
        parent: Parent Tkinter widget
        
    Returns:
        ttk.Label: Status bar label widget
    """
    status_frame = ttk.Frame(parent)
    status_frame.pack(fill=tk.X, padx=5, pady=5)
    
    status_label = ttk.Label(
        status_frame,
        text="Status: Ready",
        relief=tk.SUNKEN,
        anchor=tk.W,
        padding=5
    )
    status_label.pack(fill=tk.X)
    
    return status_label


def update_status_bar(status_bar: ttk.Label, message: str) -> None:
    """
    Update the status bar with a new message.
    
    Args:
        status_bar: Status bar label widget to update
        message (str): Message to display
    """
    status_bar.config(text=f"Status: {message}")


def format_coordinate_display(x: Optional[int], y: Optional[int]) -> str:
    """
    Format coordinate values for display in the GUI.
    
    Args:
        x (int, optional): X coordinate
        y (int, optional): Y coordinate
        
    Returns:
        str: Formatted coordinate string (e.g., "(x=100, y=200)" or "Not Set")
    """
    if x is not None and y is not None:
        return f"(x={x}, y={y})"
    return "Not Set"


def format_region_display(x: Optional[int], y: Optional[int], 
                         w: Optional[int], h: Optional[int]) -> str:
    """
    Format region values for display in the GUI.
    
    Args:
        x (int, optional): X coordinate
        y (int, optional): Y coordinate
        w (int, optional): Width
        h (int, optional): Height
        
    Returns:
        str: Formatted region string (e.g., "(x=100, y=200, w=50, h=10)" or "Not Set")
    """
    if all(v is not None for v in [x, y, w, h]):
        return f"(x={x}, y={y}, w={w}, h={h})"
    return "Not Set"
