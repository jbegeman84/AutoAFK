"""
AFK Auto-Help Module: Hunger Bar Detection Engine

This module implements the screenshot-based hunger bar detection algorithm.
It analyzes screen regions to determine the current hunger percentage using
color-based pixel classification.

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 3 (Hunger Bar Detection Engine).
"""

from typing import Optional, Tuple
import pyautogui
from PIL import Image


# Configurable detection thresholds
BRIGHTNESS_THRESHOLD = 40
"""Minimum brightness value to consider a pixel as part of the hunger bar."""
RED_DOMINANCE_FACTOR = 1.1
"""Factor by which red must exceed blue to be considered bar color."""
GREEN_RATIO_THRESHOLD = 0.9
"""Minimum ratio of red to green for bar color detection."""
PIXEL_SAMPLE_RATE = 2
"""Sample every Nth pixel for performance (2 = every other pixel)."""


def classify_pixel(r: int, g: int, b: int) -> bool:
    """
    Classify whether a pixel is part of the filled hunger bar.
    
    The hunger bar appears as orange/red when filled. This function uses
    color heuristics to detect bar pixels vs. background (dark/black).
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
        
    Returns:
        bool: True if pixel is considered part of the filled bar, False otherwise
    """
    # Calculate brightness
    brightness = (r + g + b) / 3
    
    # Too dark = background/empty bar
    if brightness < BRIGHTNESS_THRESHOLD:
        return False
    
    # Check for red/orange dominance (hunger bar colors)
    # Orange/red bars have: r > g and r > b
    if r > g * GREEN_RATIO_THRESHOLD and r > b * RED_DOMINANCE_FACTOR:
        return True
    
    return False


def read_hunger_percentage(region: Optional[Tuple[int, int, int, int]]) -> float:
    """
    Read the current hunger bar fill percentage from a screen region.
    
    Takes a screenshot of the specified region and analyzes pixel colors
    to determine what percentage of the bar is filled (orange/red).
    
    Args:
        region: Tuple (x, y, width, height) of the hunger bar region.
                If None or invalid, returns 0.0.
        
    Returns:
        float: Hunger fill level as a value from 0.0 to 1.0 (0% to 100%).
               Returns 0.0 on error or invalid region.
    """
    # Validate region
    if region is None:
        return 0.0
    
    try:
        x, y, width, height = region
        
        # Validate dimensions
        if width <= 0 or height <= 0:
            return 0.0
        
        # Capture screenshot of the region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        
        # Convert to RGB if needed
        if screenshot.mode != 'RGB':
            screenshot = screenshot.convert('RGB')
        
        # Count filled vs. total pixels
        filled_pixels = 0
        total_pixels = 0
        
        # Sample pixels for performance (scan every Nth pixel)
        for py in range(0, height, PIXEL_SAMPLE_RATE):
            for px in range(0, width, PIXEL_SAMPLE_RATE):
                r, g, b = screenshot.getpixel((px, py))
                
                if classify_pixel(r, g, b):
                    filled_pixels += 1
                total_pixels += 1
        
        # Calculate percentage
        if total_pixels == 0:
            return 0.0
        
        percentage = filled_pixels / total_pixels
        return max(0.0, min(1.0, percentage))  # Clamp to [0.0, 1.0]
        
    except Exception as e:
        # Return 0.0 on any error
        return 0.0


def detect_hunger_level(region: Optional[Tuple[int, int, int, int]]) -> Optional[float]:
    """
    Detect the current hunger level from a screen region.
    
    Legacy function name for backward compatibility.
    Returns hunger percentage as 0.0-100.0 instead of 0.0-1.0.
    
    Args:
        region (tuple): (x, y, width, height) of the hunger bar region
        
    Returns:
        float: Hunger percentage (0.0 to 100.0), or None if detection fails
    """
    percentage = read_hunger_percentage(region)
    if percentage == 0.0 and region is not None:
        # Could be a real 0% or an error - return None to indicate failure
        return None
    return percentage * 100.0


def capture_region_screenshot(region: Optional[Tuple[int, int, int, int]]) -> Optional[Image.Image]:
    """
    Capture a screenshot of the specified screen region.
    
    Args:
        region (tuple): (x, y, width, height) of the region to capture
        
    Returns:
        PIL.Image: Screenshot image of the region, or None on error
    """
    if region is None:
        return None
    
    try:
        x, y, width, height = region
        if width <= 0 or height <= 0:
            return None
        
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return screenshot
    except Exception:
        return None
