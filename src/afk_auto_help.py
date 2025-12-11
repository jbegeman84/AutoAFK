"""
AFK Auto-Help Module: Main GUI Application

This module contains the main Tkinter GUI application for AFK Auto-Help.
It serves as the entry point for the desktop automation utility.

NOTE:
This file contains the initial scaffolding for Phase 0.
Full implementation will be completed in Phase 1 (Core GUI Framework).
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Optional

from state import AppState
import ui_elements
import region_selector
import hunger_detection
import worker_threads
import threading


class AFKAutoHelpApp:
    """
    Main application class for AFK Auto-Help GUI.
    
    Manages the Tkinter window, UI elements, and application state.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.state = AppState()
        
        # Configure window
        self.root.title("AFK Auto-Help")
        self.root.minsize(800, 600)
        
        # Create main UI structure
        self._create_widgets()
        
        # Update status bar with initial state
        ui_elements.update_status_bar(self.status_bar, self.state.status_message)
    
    def safe_status_update(self, msg: str):
        """
        Thread-safe status bar update method.
        
        Worker threads should use this method to update the status bar
        from background threads. This method schedules the update on the
        main GUI thread.
        
        Args:
            msg: Status message to display
        """
        self.root.after(0, lambda: ui_elements.update_status_bar(self.status_bar, msg))
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="AFK Auto-Help",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Two main sections side by side
        sections_frame = ttk.Frame(main_container)
        sections_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left section: Hunger Auto-Feed
        self.hunger_frame = ttk.LabelFrame(
            sections_frame,
            text="Hunger Auto-Feed",
            padding="10"
        )
        self.hunger_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self._create_hunger_section()
        
        # Right section: Auto-Chop Tool
        self.chop_frame = ttk.LabelFrame(
            sections_frame,
            text="Auto-Chop Tool",
            padding="10"
        )
        self.chop_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self._create_chop_section()
        
        # Status bar
        self.status_bar = ui_elements.create_status_bar(main_container)
        
        # STOP ALL button
        stop_frame = ttk.Frame(main_container)
        stop_frame.pack(fill=tk.X, pady=10)
        
        self.stop_button = ttk.Button(
            stop_frame,
            text="STOP ALL",
            command=self._on_stop_all
        )
        self.stop_button.pack()
    
    def _create_hunger_section(self):
        """Create UI elements for the Hunger Auto-Feed section."""
        # Feed mode selection (Radio buttons)
        mode_frame = ttk.LabelFrame(self.hunger_frame, text="Feed Mode", padding="5")
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.feed_mode_var = tk.StringVar(value=self.state.feed_mode)
        
        timer_radio = ttk.Radiobutton(
            mode_frame,
            text="Timer Mode",
            variable=self.feed_mode_var,
            value="TIMER",
            command=self._on_feed_mode_changed
        )
        timer_radio.pack(anchor=tk.W, padx=5, pady=2)
        
        monitor_radio = ttk.Radiobutton(
            mode_frame,
            text="Monitor Hunger Bar Mode",
            variable=self.feed_mode_var,
            value="MONITOR_BAR",
            command=self._on_feed_mode_changed
        )
        monitor_radio.pack(anchor=tk.W, padx=5, pady=2)
        
        # Settings frame
        settings_frame = ttk.Frame(self.hunger_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Timer interval (for Timer Mode)
        timer_frame = ttk.Frame(settings_frame)
        timer_frame.pack(fill=tk.X, pady=2)
        ttk.Label(timer_frame, text="Timer Interval (minutes):").pack(side=tk.LEFT, padx=5)
        self.timer_interval_var = tk.StringVar(value=str(self.state.timer_interval_minutes))
        timer_entry = ttk.Entry(timer_frame, textvariable=self.timer_interval_var, width=10)
        timer_entry.pack(side=tk.LEFT, padx=5)
        timer_entry.bind("<FocusOut>", lambda e: self._on_timer_interval_changed())
        
        # Hunger threshold (for Monitor Mode)
        threshold_frame = ttk.Frame(settings_frame)
        threshold_frame.pack(fill=tk.X, pady=2)
        ttk.Label(threshold_frame, text="Hunger Threshold (%):").pack(side=tk.LEFT, padx=5)
        self.hunger_threshold_var = tk.StringVar(value=str(self.state.hunger_threshold))
        threshold_entry = ttk.Entry(threshold_frame, textvariable=self.hunger_threshold_var, width=10)
        threshold_entry.pack(side=tk.LEFT, padx=5)
        threshold_entry.bind("<FocusOut>", lambda e: self._on_hunger_threshold_changed())
        
        # Record Hunger Region button
        record_region_button = ttk.Button(
            self.hunger_frame,
            text="Record Hunger Region",
            command=self._on_record_hunger_region
        )
        record_region_button.pack(pady=5)
        
        # Record Feed Trigger button
        record_feed_button = ttk.Button(
            self.hunger_frame,
            text="Record Feed Trigger",
            command=self._on_record_feed_trigger
        )
        record_feed_button.pack(pady=5)
        
        # Debug mode checkbox
        debug_frame = ttk.Frame(self.hunger_frame)
        debug_frame.pack(fill=tk.X, pady=5)
        self.debug_mode_var = tk.BooleanVar(value=False)
        debug_checkbox = ttk.Checkbutton(
            debug_frame,
            text="Debug Hunger Detection",
            variable=self.debug_mode_var
        )
        debug_checkbox.pack(anchor=tk.W, padx=5)
        
        # Test Hunger Bar button
        test_hunger_button = ttk.Button(
            self.hunger_frame,
            text="Test Hunger Bar",
            command=self._on_test_hunger_bar
        )
        test_hunger_button.pack(pady=5)
        
        # Start Auto-Feed button
        start_feed_button = ttk.Button(
            self.hunger_frame,
            text="Start Auto-Feed",
            command=self._on_start_auto_feed
        )
        start_feed_button.pack(pady=5)
        
        # Display saved values
        info_frame = ttk.Frame(self.hunger_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        # Current hunger percentage label
        self.current_hunger_label = ttk.Label(
            info_frame,
            text="Current Hunger: --%",
            font=('Arial', 10, 'bold')
        )
        self.current_hunger_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.feed_trigger_label = ttk.Label(
            info_frame,
            text=f"Feed Trigger: {ui_elements.format_coordinate_display(*self.state.feed_trigger) if self.state.feed_trigger else 'Not Set'}"
        )
        self.feed_trigger_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.hunger_region_label = ttk.Label(
            info_frame,
            text=f"Hunger Region: {ui_elements.format_region_display(*self.state.hunger_region) if self.state.hunger_region else 'Not Set'}"
        )
        self.hunger_region_label.pack(anchor=tk.W, padx=5, pady=2)
    
    def _create_chop_section(self):
        """Create UI elements for the Auto-Chop Tool section."""
        # Chop click rate
        rate_frame = ttk.Frame(self.chop_frame)
        rate_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rate_frame, text="Chop Click Rate (clicks/sec):").pack(side=tk.LEFT, padx=5)
        self.chop_rate_var = tk.StringVar(value=str(self.state.chop_click_rate))
        rate_entry = ttk.Entry(rate_frame, textvariable=self.chop_rate_var, width=10)
        rate_entry.pack(side=tk.LEFT, padx=5)
        rate_entry.bind("<FocusOut>", lambda e: self._on_chop_rate_changed())
        
        # Chop duration
        duration_frame = ttk.Frame(self.chop_frame)
        duration_frame.pack(fill=tk.X, pady=5)
        ttk.Label(duration_frame, text="Chop Duration (seconds):").pack(side=tk.LEFT, padx=5)
        self.chop_duration_var = tk.StringVar(value=str(self.state.chop_duration))
        duration_entry = ttk.Entry(duration_frame, textvariable=self.chop_duration_var, width=10)
        duration_entry.pack(side=tk.LEFT, padx=5)
        duration_entry.bind("<FocusOut>", lambda e: self._on_chop_duration_changed())
        
        # Record Chop Trigger button
        record_chop_button = ttk.Button(
            self.chop_frame,
            text="Record Chop Trigger",
            command=self._on_record_chop_trigger
        )
        record_chop_button.pack(pady=5)
        
        # Start/Stop Auto-Chop button
        self.auto_chop_button = ttk.Button(
            self.chop_frame,
            text="Start Auto-Chop",
            command=self._on_auto_chop_button_pressed
        )
        self.auto_chop_button.pack(pady=5)
        
        # Display saved trigger
        info_frame = ttk.Frame(self.chop_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.chop_trigger_label = ttk.Label(
            info_frame,
            text=f"Chop Trigger: {ui_elements.format_coordinate_display(*self.state.chop_trigger) if self.state.chop_trigger else 'Not Set'}"
        )
        self.chop_trigger_label.pack(anchor=tk.W, padx=5, pady=2)
    
    # Event handlers (placeholder implementations)
    
    def _on_feed_mode_changed(self):
        """Handle feed mode radio button change."""
        self.state.feed_mode = self.feed_mode_var.get()
        ui_elements.update_status_bar(
            self.status_bar,
            f"Feed mode changed to: {self.state.feed_mode}"
        )
    
    def _on_timer_interval_changed(self):
        """Handle timer interval entry change."""
        try:
            value = float(self.timer_interval_var.get())
            if value > 0:
                self.state.timer_interval_minutes = value
                ui_elements.update_status_bar(
                    self.status_bar,
                    f"Timer interval set to: {value} minutes"
                )
            else:
                ui_elements.update_status_bar(self.status_bar, "Timer interval must be positive")
        except ValueError:
            ui_elements.update_status_bar(self.status_bar, "Invalid timer interval value")
    
    def _on_hunger_threshold_changed(self):
        """Handle hunger threshold entry change."""
        try:
            value = float(self.hunger_threshold_var.get())
            if 0 <= value <= 100:
                self.state.hunger_threshold = value
                ui_elements.update_status_bar(
                    self.status_bar,
                    f"Hunger threshold set to: {value}%"
                )
            else:
                ui_elements.update_status_bar(self.status_bar, "Hunger threshold must be 0-100")
        except ValueError:
            ui_elements.update_status_bar(self.status_bar, "Invalid hunger threshold value")
    
    def _on_test_hunger_bar(self):
        """Handle Test Hunger Bar button click."""
        # Check if hunger region is set
        if self.state.hunger_region is None:
            ui_elements.update_status_bar(
                self.status_bar,
                "Error: No hunger region selected. Please record a hunger region first."
            )
            # Show error dialog
            messagebox.showerror(
                "No Hunger Region",
                "Please record a hunger region before testing detection."
            )
            return
        
        # Perform hunger detection
        try:
            hunger_percentage = hunger_detection.read_hunger_percentage(self.state.hunger_region)
            hunger_percent = hunger_percentage * 100.0
            
            # Update GUI labels
            self.current_hunger_label.config(
                text=f"Current Hunger: {hunger_percent:.1f}%"
            )
            
            # Update status bar
            ui_elements.update_status_bar(
                self.status_bar,
                f"Hunger detected: {hunger_percent:.1f}%"
            )
            
            # Debug mode: show additional info
            if self.debug_mode_var.get():
                threshold_status = "BELOW" if hunger_percent < self.state.hunger_threshold else "ABOVE"
                ui_elements.update_status_bar(
                    self.status_bar,
                    f"Hunger: {hunger_percent:.1f}% ({threshold_status} threshold of {self.state.hunger_threshold}%)"
                )
                
        except Exception as e:
            ui_elements.update_status_bar(
                self.status_bar,
                f"Error detecting hunger: {str(e)}"
            )
            self.current_hunger_label.config(text="Current Hunger: Error")
    
    def _on_record_hunger_region(self):
        """Handle Record Hunger Region button click."""
        region_selector.select_region(self._handle_hunger_region_selected)
    
    def _handle_hunger_region_selected(self, region):
        """
        Handle hunger region selection callback.
        
        Args:
            region: Tuple (x, y, width, height) or None if cancelled
        """
        if region is not None:
            self.state.hunger_region = region
            region_text = ui_elements.format_region_display(*region)
            self.hunger_region_label.config(
                text=f"Hunger Region: {region_text}"
            )
            ui_elements.update_status_bar(
                self.status_bar,
                f"Hunger region recorded: {region_text}"
            )
        else:
            ui_elements.update_status_bar(
                self.status_bar,
                "Hunger region selection cancelled"
            )
    
    def _on_record_feed_trigger(self):
        """Handle Record Feed Trigger button click."""
        region_selector.select_point(self._handle_feed_trigger_selected)
    
    def _handle_feed_trigger_selected(self, point):
        """
        Handle feed trigger point selection callback.
        
        Args:
            point: Tuple (x, y) or None if cancelled
        """
        if point is not None:
            x, y = point
            self.state.feed_trigger = (x, y)
            coord_text = ui_elements.format_coordinate_display(x, y)
            self.feed_trigger_label.config(
                text=f"Feed Trigger: {coord_text}"
            )
            ui_elements.update_status_bar(
                self.status_bar,
                f"Feed trigger recorded: {coord_text}"
            )
        else:
            ui_elements.update_status_bar(
                self.status_bar,
                "Feed trigger selection cancelled"
            )
    
    def _on_record_chop_trigger(self):
        """Handle Record Chop Trigger button click."""
        region_selector.select_point(self._handle_chop_trigger_selected)
    
    def _handle_chop_trigger_selected(self, point):
        """
        Handle chop trigger point selection callback.
        
        Args:
            point: Tuple (x, y) or None if cancelled
        """
        if point is not None:
            x, y = point
            self.state.chop_trigger = (x, y)
            coord_text = ui_elements.format_coordinate_display(x, y)
            self.chop_trigger_label.config(
                text=f"Chop Trigger: {coord_text}"
            )
            ui_elements.update_status_bar(
                self.status_bar,
                f"Chop trigger recorded: {coord_text}"
            )
        else:
            ui_elements.update_status_bar(
                self.status_bar,
                "Chop trigger selection cancelled"
            )
    
    def _on_auto_chop_button_pressed(self):
        """Handle Auto-Chop button click (Start/Stop toggle)."""
        if self.state.chop_running:
            # This is a stop request
            self.state.chop_running = False
            self.state.stop_all_flag = True  # Also set global stop flag
            ui_elements.update_status_bar(
                self.status_bar,
                "Stopping auto-chop..."
            )
            # Button text will be updated by on_chop_worker_finished()
        else:
            # This is a start request
            # Validate required settings
            if self.state.chop_trigger is None:
                messagebox.showerror(
                    "Missing Configuration",
                    "Chop trigger coordinate is required.\n"
                    "Please record a chop trigger first."
                )
                return
            
            if self.state.chop_click_rate <= 0:
                messagebox.showerror(
                    "Invalid Configuration",
                    "Chop click rate must be greater than 0."
                )
                return
            
            if self.state.chop_duration <= 0:
                messagebox.showerror(
                    "Invalid Configuration",
                    "Chop duration must be greater than 0."
                )
                return
            
            # Update state
            self.state.chop_running = True
            self.state.stop_all_flag = False  # Clear global stop flag
            
            # Update button text
            self.auto_chop_button.config(text="Stop Auto-Chop")
            
            # Update status
            ui_elements.update_status_bar(
                self.status_bar,
                "Preparing to auto-chop..."
            )
            
            # Create and start worker thread
            thread = threading.Thread(
                target=worker_threads.auto_chop_worker,
                args=(self, self.state),
                daemon=True
            )
            self.state.chop_worker_thread = thread
            thread.start()
    
    def on_chop_worker_finished(self):
        """
        Called by the auto-chop worker when it finishes.
        Must be safe to call from a worker thread.
        """
        def _finish():
            self.state.chop_running = False
            self.state.chop_worker_thread = None
            self.auto_chop_button.config(text="Start Auto-Chop")
            self.safe_status_update("Auto-chop idle")
        
        self.root.after(0, _finish)
    
    def _on_chop_rate_changed(self):
        """Handle chop click rate entry change."""
        try:
            value = float(self.chop_rate_var.get())
            # Clamp to sane range (minimum 0.1 clicks/sec)
            if value < 0.1:
                value = 0.1
                self.chop_rate_var.set(str(value))
                messagebox.showerror(
                    "Invalid Value",
                    "Chop click rate must be at least 0.1 clicks/sec. Value adjusted."
                )
            
            if value > 0:
                self.state.chop_click_rate = value
                ui_elements.update_status_bar(
                    self.status_bar,
                    f"Chop click rate set to: {value} clicks/sec"
                )
            else:
                # Revert to previous valid value
                self.chop_rate_var.set(str(self.state.chop_click_rate))
                messagebox.showerror(
                    "Invalid Value",
                    "Chop click rate must be positive."
                )
        except ValueError:
            # Revert to previous valid value
            self.chop_rate_var.set(str(self.state.chop_click_rate))
            messagebox.showerror(
                "Invalid Value",
                "Chop click rate must be a number."
            )
    
    def _on_chop_duration_changed(self):
        """Handle chop duration entry change."""
        try:
            value = float(self.chop_duration_var.get())
            # Clamp to sane range (minimum 1 second)
            if value < 1.0:
                value = 1.0
                self.chop_duration_var.set(str(int(value)))
                messagebox.showerror(
                    "Invalid Value",
                    "Chop duration must be at least 1 second. Value adjusted."
                )
            
            if value > 0:
                self.state.chop_duration = value
                ui_elements.update_status_bar(
                    self.status_bar,
                    f"Chop duration set to: {value} seconds"
                )
            else:
                # Revert to previous valid value
                self.chop_duration_var.set(str(self.state.chop_duration))
                messagebox.showerror(
                    "Invalid Value",
                    "Chop duration must be positive."
                )
        except ValueError:
            # Revert to previous valid value
            self.chop_duration_var.set(str(self.state.chop_duration))
            messagebox.showerror(
                "Invalid Value",
                "Chop duration must be a number."
            )
    
    def _on_start_auto_feed(self):
        """Handle Start Auto-Feed button click."""
        # Check if a worker is already running
        if self.state.worker_thread is not None:
            messagebox.showwarning(
                "Worker Already Running",
                "A worker thread is already running. Please stop it first."
            )
            return
        
        # Validate required settings based on feed mode
        if self.state.feed_mode == "MONITOR_BAR":
            # Monitor mode requires hunger region
            if self.state.hunger_region is None:
                messagebox.showerror(
                    "Missing Configuration",
                    "Monitor mode requires a hunger region to be set.\n"
                    "Please record a hunger region first."
                )
                return
        
        # Both modes require feed trigger
        if self.state.feed_trigger is None:
            messagebox.showerror(
                "Missing Configuration",
                "Feed trigger coordinate is required.\n"
                "Please record a feed trigger first."
            )
            return
        
        # Reset stop flag
        self.state.stop_all_flag = False
        
        # Start appropriate worker thread based on feed mode
        if self.state.feed_mode == "TIMER":
            # Validate timer interval
            if self.state.timer_interval_minutes <= 0:
                messagebox.showerror(
                    "Invalid Configuration",
                    "Timer interval must be greater than 0."
                )
                return
            
            # Create and start timer worker thread
            thread = threading.Thread(
                target=worker_threads.timer_feed_worker,
                args=(self, self.state),
                daemon=True
            )
            self.state.worker_thread = thread
            thread.start()
            ui_elements.update_status_bar(
                self.status_bar,
                f"Timer mode started: feeding every {self.state.timer_interval_minutes} minutes"
            )
            
        elif self.state.feed_mode == "MONITOR_BAR":
            # Validate hunger threshold
            if self.state.hunger_threshold < 0 or self.state.hunger_threshold > 100:
                messagebox.showerror(
                    "Invalid Configuration",
                    "Hunger threshold must be between 0 and 100."
                )
                return
            
            # Create and start hunger monitor worker thread
            thread = threading.Thread(
                target=worker_threads.hunger_monitor_worker,
                args=(self, self.state),
                daemon=True
            )
            self.state.worker_thread = thread
            thread.start()
            ui_elements.update_status_bar(
                self.status_bar,
                f"Hunger monitoring started: feeding when hunger ≤ {self.state.hunger_threshold}%"
            )
    
    def _on_stop_all(self):
        """Handle STOP ALL button click."""
        # Check if any worker is running
        has_worker = (self.state.worker_thread is not None) or (self.state.chop_worker_thread is not None)
        
        if not has_worker:
            ui_elements.update_status_bar(
                self.status_bar,
                "No worker thread running"
            )
            return
        
        # Set stop flags for all workers
        self.state.stop_all_flag = True
        self.state.chop_running = False  # Also stop auto-chop
        
        ui_elements.update_status_bar(
            self.status_bar,
            "Stopping all workers..."
        )
        
        # Try to join hunger feed worker thread (with timeout)
        if self.state.worker_thread is not None:
            try:
                self.state.worker_thread.join(timeout=2.0)
            except Exception:
                pass  # Thread may have already finished
            self.state.worker_thread = None
        
        # Try to join auto-chop worker thread (with timeout)
        if self.state.chop_worker_thread is not None:
            try:
                self.state.chop_worker_thread.join(timeout=2.0)
            except Exception:
                pass  # Thread may have already finished
            self.state.chop_worker_thread = None
        
        # Reset flags for next start
        self.state.stop_all_flag = False
        self.state.chop_running = False
        
        # Update button text if auto-chop was running
        if hasattr(self, 'auto_chop_button'):
            self.auto_chop_button.config(text="Start Auto-Chop")
        
        ui_elements.update_status_bar(
            self.status_bar,
            "Ready"
        )


def main():
    """
    Main entry point for the AFK Auto-Help application.
    
    This function will initialize and run the Tkinter GUI.
    """
    root = tk.Tk()
    app = AFKAutoHelpApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
