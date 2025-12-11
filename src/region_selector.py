"""
AFK Auto-Help Module: Screen Region Selector

This module provides a transparent fullscreen overlay for selecting
screen regions (e.g., hunger bar area) and capturing click coordinates
for trigger points (feed trigger, chop trigger).

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 2 (Screen Region & Click Recording).
"""

import tkinter as tk
from typing import Optional, Callable, Tuple

# TODO: Phase 4+ - pyautogui will be needed for automation actions
import pyautogui


def select_region(callback: Callable[[Tuple[int, int, int, int]], None]) -> None:
    """
    Display a fullscreen overlay for selecting a screen region.
    
    Creates a transparent fullscreen window that allows the user to click
    and drag to define a rectangle. On mouse release, computes the region
    coordinates and calls the callback.
    
    Args:
        callback: Function to call with (x, y, width, height) tuple when
                 region is selected, or None if cancelled
    """
    # Create fullscreen overlay window (without using -fullscreen to avoid macOS fullscreen API)
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)  # Remove window decorations first
    overlay.attributes('-topmost', True)
    overlay.attributes('-alpha', 0.3)  # Semi-transparent background
    overlay.configure(bg='black')
    
    # Get screen dimensions BEFORE setting geometry
    screen_width = overlay.winfo_screenwidth()
    screen_height = overlay.winfo_screenheight()
    
    # Manually set window to cover entire screen (avoid -fullscreen attribute)
    overlay.geometry(f'{screen_width}x{screen_height}+0+0')
    
    # Create canvas for drawing selection rectangle
    canvas = tk.Canvas(
        overlay,
        bg='black',
        highlightthickness=0,
        cursor='crosshair'
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Selection state
    start_x = None
    start_y = None
    start_canvas_x = None
    start_canvas_y = None
    rect_id = None
    
    def on_button_press(event):
        """Handle mouse button press - start selection."""
        nonlocal start_x, start_y, start_canvas_x, start_canvas_y, rect_id
        # Store both root (for final calculation) and canvas (for drawing) coordinates
        start_x = event.x_root  # Screen coordinates for final calculation
        start_y = event.y_root
        start_canvas_x = event.x  # Canvas coordinates for drawing
        start_canvas_y = event.y
        # Clear any existing rectangle
        if rect_id is not None:
            canvas.delete(rect_id)
    
    def on_motion(event):
        """Handle mouse motion - update selection rectangle."""
        nonlocal rect_id, start_canvas_x, start_canvas_y
        if start_canvas_x is not None and start_canvas_y is not None:
            # Clear previous rectangle
            if rect_id is not None:
                canvas.delete(rect_id)
            
            # Draw new rectangle using canvas coordinates (relative to canvas widget)
            canvas_x1 = start_canvas_x
            canvas_y1 = start_canvas_y
            canvas_x2 = event.x
            canvas_y2 = event.y
            
            # Use canvas coordinates for drawing
            rect_id = canvas.create_rectangle(
                canvas_x1, canvas_y1, canvas_x2, canvas_y2,
                outline='cyan', width=2, fill='', stipple='gray50'
            )
    
    def on_button_release(event):
        """Handle mouse button release - finalize selection."""
        nonlocal start_x, start_y
        if start_x is not None and start_y is not None:
            # Use root coordinates for final calculation (screen coordinates)
            end_x = event.x_root
            end_y = event.y_root
            
            # Calculate region coordinates (always use root coordinates)
            x = min(start_x, end_x)
            y = min(start_y, end_y)
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)
            
            # Only accept if region has meaningful size
            if width > 5 and height > 5:
                region = (x, y, width, height)
                overlay.destroy()
                callback(region)
            else:
                # Too small, cancel
                overlay.destroy()
                callback(None)
        else:
            overlay.destroy()
            callback(None)
    
    def on_escape(event):
        """Handle Escape key - cancel selection."""
        overlay.destroy()
        callback(None)
    
    def on_close():
        """Handle window close - cancel selection."""
        overlay.destroy()
        callback(None)
    
    # Bind events
    canvas.bind('<Button-1>', on_button_press)
    canvas.bind('<B1-Motion>', on_motion)
    canvas.bind('<ButtonRelease-1>', on_button_release)
    overlay.bind('<Escape>', on_escape)
    overlay.protocol('WM_DELETE_WINDOW', on_close)
    
    # Add instruction text
    instruction = tk.Label(
        overlay,
        text="Click and drag to select region. Press ESC to cancel.",
        bg='black',
        fg='white',
        font=('Arial', 14)
    )
    instruction.place(x=screen_width // 2, y=50, anchor=tk.CENTER)
    
    # Focus the overlay to capture keyboard events
    overlay.focus_force()


def select_point(callback: Callable[[Optional[Tuple[int, int]]], None]) -> None:
    """
    Display a fullscreen overlay that captures a single click coordinate.
    
    Creates a transparent fullscreen window. When the user clicks once,
    captures the global mouse coordinates and calls the callback.
    
    Args:
        callback: Function to call with (x, y) tuple when point is clicked,
                 or None if cancelled
    """
    # Create fullscreen overlay window (without using -fullscreen to avoid macOS fullscreen API)
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)  # Remove window decorations first
    overlay.attributes('-topmost', True)
    overlay.attributes('-alpha', 0.2)  # Semi-transparent background
    overlay.configure(bg='black')
    
    # Get screen dimensions BEFORE setting geometry
    screen_width = overlay.winfo_screenwidth()
    screen_height = overlay.winfo_screenheight()
    
    # Manually set window to cover entire screen (avoid -fullscreen attribute)
    overlay.geometry(f'{screen_width}x{screen_height}+0+0')
    
    # Create canvas
    canvas = tk.Canvas(
        overlay,
        bg='black',
        highlightthickness=0,
        cursor='crosshair'
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Track mouse position for visual feedback
    crosshair_h = None
    crosshair_v = None
    
    def on_motion(event):
        """Handle mouse motion - update crosshair."""
        nonlocal crosshair_h, crosshair_v
        # Clear previous crosshair
        if crosshair_h is not None:
            canvas.delete(crosshair_h)
            canvas.delete(crosshair_v)
        
        # Draw crosshair at mouse position (use canvas coordinates)
        x = event.x
        y = event.y
        crosshair_h = canvas.create_line(
            x - 20, y, x + 20, y,
            fill='cyan', width=2
        )
        crosshair_v = canvas.create_line(
            x, y - 20, x, y + 20,
            fill='cyan', width=2
        )
    
    def on_click(event):
        """Handle mouse click - capture coordinate."""
        x = event.x_root
        y = event.y_root
        overlay.destroy()
        callback((x, y))
    
    def on_escape(event):
        """Handle Escape key - cancel selection."""
        overlay.destroy()
        callback(None)
    
    def on_close():
        """Handle window close - cancel selection."""
        overlay.destroy()
        callback(None)
    
    # Bind events
    canvas.bind('<Motion>', on_motion)
    canvas.bind('<Button-1>', on_click)
    overlay.bind('<Escape>', on_escape)
    overlay.protocol('WM_DELETE_WINDOW', on_close)
    
    # Add instruction text
    instruction = tk.Label(
        overlay,
        text="Click to select point. Press ESC to cancel.",
        bg='black',
        fg='white',
        font=('Arial', 14)
    )
    instruction.place(x=screen_width // 2, y=50, anchor=tk.CENTER)
    
    # Focus the overlay to capture keyboard events
    overlay.focus_force()


# Legacy function name for backward compatibility
def capture_click_coordinate(callback: Callable[[Optional[Tuple[int, int]]], None]) -> None:
    """
    Legacy function name for select_point.
    
    This function is kept for backward compatibility but select_point
    should be used instead.
    """
    select_point(callback)
