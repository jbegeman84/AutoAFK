"""
AFK Auto-Help Module: Application State Management

This module defines the AppState class that stores all critical application
data including configuration settings, screen regions, coordinates, and
automation parameters.

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 1 (Core GUI Framework).
"""

from typing import Optional, Tuple


# TODO: Phase 7 - Add settings persistence (save/load to file)


class AppState:
    """
    Stores all critical application state and configuration data.
    
    This class maintains the current settings for hunger detection,
    automation parameters, and user-configured regions/coordinates.
    """
    
    def __init__(self):
        """
        Initialize AppState with default values.
        
        All attributes will be set to None or default values initially.
        """
        # Hunger detection settings
        self.hunger_region: Optional[Tuple[int, int, int, int]] = None
        """Hunger bar screen region as (x, y, width, height). Set in Phase 2."""
        
        self.hunger_threshold: float = 10.0
        """Hunger threshold percentage (0-100). Feed when hunger drops below this value."""
        
        self.feed_mode: str = "TIMER"
        """Feed mode: "TIMER" for interval-based feeding, "MONITOR_BAR" for hunger-based feeding."""
        
        self.feed_trigger: Optional[Tuple[int, int]] = None
        """Feed trigger coordinate as (x, y). Set in Phase 2. User should position stew and click on it."""
        
        # Timer mode settings
        self.timer_interval_minutes: float = 5.0
        """Timer interval in minutes for timer-based feeding mode."""
        
        # Auto-chop settings
        self.chop_trigger: Optional[Tuple[int, int]] = None
        """Chop trigger coordinate as (x, y). Set in Phase 2."""
        
        self.chop_click_rate: float = 1.0
        """Auto-chop click rate in clicks per second."""
        
        self.chop_duration: float = 20.0
        """Auto-chop duration in seconds."""
        
        # Status
        self.status_message: str = "Ready"
        """Current status message displayed in the status bar."""
        
        # Thread control (Phase 4)
        self.stop_all_flag: bool = False
        """Flag to signal all worker threads to stop."""
        
        self.worker_thread: Optional[object] = None
        """Reference to the currently running worker thread, if any."""
    
    def __repr__(self) -> str:
        """Return a string representation of AppState for debugging."""
        return (
            f"AppState("
            f"hunger_region={self.hunger_region}, "
            f"hunger_threshold={self.hunger_threshold}, "
            f"feed_mode={self.feed_mode}, "
            f"feed_trigger={self.feed_trigger}, "
            f"timer_interval_minutes={self.timer_interval_minutes}, "
            f"chop_trigger={self.chop_trigger}, "
            f"chop_click_rate={self.chop_click_rate}, "
            f"chop_duration={self.chop_duration}, "
            f"status_message='{self.status_message}'"
            f")"
        )
