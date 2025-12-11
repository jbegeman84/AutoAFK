"""
AFK Auto-Help Module: Background Worker Threads

This module contains worker thread classes for running automation tasks
in the background without blocking the GUI. Includes threads for:
- Timer-based feeding
- Hunger monitoring and auto-feeding
- Auto-chop automation

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 4 (Hunger Auto-Feed Logic)
and Phase 5 (Auto-Chop Tool).
"""

import threading
import time
import pyautogui
from typing import Optional

import hunger_detection

# TODO: Phase 5 - Implement Auto-Chop worker thread


def perform_feed(state):
    """
    Perform the feed action: click the feed trigger point.
    
    User should have already selected the stew item and positioned it
    so the trigger point is clickable. This function only clicks.
    
    Args:
        state: AppState instance with feed configuration
        
    Returns:
        bool: True if feed was successful, False otherwise
    """
    try:
        # Validate required settings
        if state.feed_trigger is None:
            return False
        
        # Click at the feed trigger point (user should have stew selected already)
        x, y = state.feed_trigger
        pyautogui.click(x, y)
        
        return True
    except Exception as e:
        # Log error but don't crash
        print(f"Error in perform_feed: {e}")
        return False


def timer_feed_worker(app, state):
    """
    Timer-based feeding worker thread.
    
    Feeds the character at regular intervals (every X minutes).
    Runs until state.stop_all_flag is True.
    
    Args:
        app: AFKAutoHelpApp instance for safe UI updates
        state: AppState instance with configuration
    """
    # Convert interval from minutes to seconds
    interval_seconds = state.timer_interval_minutes * 60
    
    app.safe_status_update(f"Timer mode: waiting {state.timer_interval_minutes} minutes")
    
    while not state.stop_all_flag:
        # Sleep for the interval, but check stop flag periodically
        sleep_chunks = int(interval_seconds / 1.0)  # Check every second
        for _ in range(sleep_chunks):
            if state.stop_all_flag:
                break
            time.sleep(1.0)
        
        # Check stop flag before feeding
        if state.stop_all_flag:
            break
        
        # Perform feed action
        app.safe_status_update("Performing feed action...")
        success = perform_feed(state)
        
        if success:
            app.safe_status_update(f"Feed complete. Next feed in {state.timer_interval_minutes} minutes")
        else:
            app.safe_status_update("Feed failed - check settings")
        
        # Brief delay before next cycle
        time.sleep(0.5)
    
    # Worker stopped
    app.safe_status_update("Timer worker stopped")
    state.worker_thread = None


def hunger_monitor_worker(app, state):
    """
    Hunger monitoring worker thread.
    
    Continuously monitors the hunger bar and feeds when threshold is reached.
    Runs until state.stop_all_flag is True.
    
    Args:
        app: AFKAutoHelpApp instance for safe UI updates
        state: AppState instance with configuration
    """
    # Validate hunger region is set
    if state.hunger_region is None:
        app.safe_status_update("Error: No hunger region set for monitoring")
        state.worker_thread = None
        return
    
    app.safe_status_update("Hunger monitoring started")
    
    while not state.stop_all_flag:
        try:
            # Read current hunger percentage
            hunger_percentage = hunger_detection.read_hunger_percentage(state.hunger_region)
            hunger_percent = hunger_percentage * 100.0
            
            # Update GUI with current hunger
            app.safe_status_update(f"Hunger detected: {hunger_percent:.1f}%")
            
            # Update current hunger label
            app.root.after(0, lambda p=hunger_percent: app.current_hunger_label.config(
                text=f"Current Hunger: {p:.1f}%"
            ))
            
            # Check if hunger is below threshold
            if hunger_percent <= state.hunger_threshold:
                app.safe_status_update(f"Hunger low ({hunger_percent:.1f}%), feeding...")
                
                # Perform feed action
                success = perform_feed(state)
                
                if success:
                    app.safe_status_update(f"Feed complete. Hunger: {hunger_percent:.1f}%")
                else:
                    app.safe_status_update("Feed failed - check settings")
                
                # Wait a bit after feeding before checking again
                time.sleep(2.0)
            else:
                # Hunger is above threshold, wait before next check
                time.sleep(1.5)
            
            # Check stop flag
            if state.stop_all_flag:
                break
                
        except Exception as e:
            app.safe_status_update(f"Error in hunger monitoring: {str(e)}")
            time.sleep(2.0)  # Wait before retrying
    
    # Worker stopped
    app.safe_status_update("Hunger monitor stopped")
    state.worker_thread = None


# Legacy class-based implementations (kept for backward compatibility)
class TimerFeedWorker(threading.Thread):
    """
    Worker thread for timer-based feeding automation.
    
    Feeds the character at regular intervals regardless of hunger level.
    """
    
    def __init__(self, app, state):
        """
        Initialize the timer feed worker.
        
        Args:
            app: AFKAutoHelpApp instance
            state: AppState instance with configuration
        """
        super().__init__(daemon=True)
        self.app = app
        self.state = state
    
    def run(self):
        """Execute the timer-based feeding loop."""
        timer_feed_worker(self.app, self.state)
    
    def stop(self):
        """Stop the worker thread gracefully."""
        self.state.stop_all_flag = True


class HungerMonitorWorker(threading.Thread):
    """
    Worker thread for hunger bar monitoring and auto-feeding.
    
    Continuously monitors the hunger bar and feeds when threshold is reached.
    """
    
    def __init__(self, app, state):
        """
        Initialize the hunger monitor worker.
        
        Args:
            app: AFKAutoHelpApp instance
            state: AppState instance with configuration
        """
        super().__init__(daemon=True)
        self.app = app
        self.state = state
    
    def run(self):
        """Execute the hunger monitoring loop."""
        hunger_monitor_worker(self.app, self.state)
    
    def stop(self):
        """Stop the worker thread gracefully."""
        self.state.stop_all_flag = True


def auto_chop_worker(app, state):
    """
    Auto-chop worker thread function.
    
    Clicks at state.chop_trigger at a rate of state.chop_click_rate
    for state.chop_duration seconds, or until stopped.
    This runs in a background thread.
    
    Args:
        app: AFKAutoHelpApp instance for safe UI updates
        state: AppState instance with configuration
    """
    # Validate preconditions
    if state.chop_trigger is None:
        app.safe_status_update("Chop trigger not set")
        app.on_chop_worker_finished()
        return
    
    if state.chop_click_rate <= 0:
        app.safe_status_update("Invalid chop click rate")
        app.on_chop_worker_finished()
        return
    
    if state.chop_duration <= 0:
        app.safe_status_update("Invalid chop duration")
        app.on_chop_worker_finished()
        return
    
    try:
        x, y = state.chop_trigger
        click_interval = 1.0 / state.chop_click_rate
        end_time = time.time() + state.chop_duration
        
        app.safe_status_update(f"Auto-chop started: {state.chop_click_rate} clicks/sec for {state.chop_duration}s")
        
        while time.time() < end_time:
            # Check stop conditions
            if state.stop_all_flag or not state.chop_running:
                break
            
            # Perform click
            pyautogui.click(x, y)
            
            # Sleep for the click interval
            time.sleep(click_interval)
        
        # Worker finished
        if state.stop_all_flag or not state.chop_running:
            app.safe_status_update("Auto-chop stopped")
        else:
            app.safe_status_update("Auto-chop finished")
        
    except Exception as e:
        app.safe_status_update(f"Error in auto-chop: {str(e)}")
    finally:
        # Always call finished callback
        app.on_chop_worker_finished()


class AutoChopWorker(threading.Thread):
    """
    Worker thread for auto-chop automation.
    
    Performs automated clicking at the chop trigger point.
    """
    
    def __init__(self, app, state):
        """
        Initialize the auto-chop worker.
        
        Args:
            app: AFKAutoHelpApp instance
            state: AppState instance with configuration
        """
        super().__init__(daemon=True)
        self.app = app
        self.state = state
    
    def run(self):
        """Execute the auto-chop clicking loop."""
        auto_chop_worker(self.app, self.state)
    
    def stop(self):
        """Stop the worker thread gracefully."""
        self.state.chop_running = False
        self.state.stop_all_flag = True
