
# 📘 **AFK Auto-Help – Development Plan**

**Project Goal:**  
Create a macOS desktop utility that automates simple on-screen actions for Roblox gameplay (e.g., feeding based on hunger bar detection, timed clicking loops, and auto-chopping), with an easy-to-use GUI and configurable settings.

**Tech Stack:**  
- **Language:** Python 3  
- **GUI Framework:** Tkinter  
- **Screen Interaction:** PyAutoGUI + Pillow  
- **OS:** macOS (M1/M2/M3 compatible)  
- **Distribution:** Open-source on GitHub (MIT License)

---

# 🧱 **Phase 0 — Project Setup**

### 0.1 Repository Initialization
- Create GitHub repository (**completed**)
- Add:
  - `LICENSE` (MIT License)
  - `README.md`
  - `planning/` folder
  - `src/` folder for code

### 0.2 Environment Setup
- Ensure both Macs (yours and your daughter’s) have:
  - Python 3.10+  
  - `pip install pyautogui pillow`
- macOS privacy permissions:
  - Screen Recording
  - Input Monitoring

### 0.3 App Architecture Outline
- One main GUI file: `afk_auto_help.py`
- Internal helper modules:
  - `region_selector.py`
  - `worker_threads.py`
  - `state.py` (stores user settings/config)
  - `hunger_detection.py`
  - `ui_elements.py` (optional for cleaner code)

---

# 🥅 **Phase 1 — Core GUI Framework**

### 1.1 Build Base Window
- `Tk()` root window  
- Custom window title: **AFK Auto-Help**
- Two main sections:
  1. Hunger Auto-Feed  
  2. Auto-Chop Tool  
- Global **STOP ALL** button

### 1.2 Create AppState Class
Stores all critical data:

- Hunger bar region: `(x, y, w, h)`
- Hunger threshold (%)
- Mode: `TIMER` or `MONITOR_BAR`
- Feed trigger coordinate
- Stew hotkey
- Timer interval (minutes/seconds)
- Chop trigger coordinate
- Chop click rate
- Chop duration

### 1.3 Build Input Fields + Labels
- Radio buttons for feed mode selection
- Entries for:
  - Stew hotkey  
  - Timer interval  
  - Threshold percentage  
  - Chop click rate  
  - Chop duration
- A status bar at bottom to show:
  - Current hunger %
  - Active automation status

---

# 🖱️ **Phase 2 — Screen Region & Click Recording**

### 2.1 Region Selector Overlay
A transparent fullscreen overlay for selecting hunger bar area.

### 2.2 Coordinate Capture for Trigger Points
For:
- Feed trigger point  
- Chop trigger point  

Overlay listens for a single click and records `(x, y)`.

### 2.3 Visual Feedback
- Display coordinates in the GUI
- Example:
  - “Hunger Region Set: (x=…, y=…, w=…, h=…)”
  - “Feed Trigger: (x=…, y=…)”

---

# 🔍 **Phase 3 — Hunger Bar Detection Engine**

### 3.1 Implement Screenshot Reader

### 3.2 Implement Color-Based Pixel Classification

### 3.3 Make Threshold User-Configurable

### 3.4 Debug Mode (Optional)

---

# 🍲 **Phase 4 — Hunger Auto-Feed Logic**

### 4.1 Implement “Perform Feed” Action

### 4.2 Implement Timer Mode Worker Thread

### 4.3 Implement Hunger Monitoring Mode Worker

### 4.4 Thread Handling

### 4.5 Update GUI Status in Real Time

---

# 🪓 **Phase 5 — Auto-Chop Tool**

### 5.1 Input Fields

### 5.2 Perform Auto-Chop Action

### 5.3 Clean Start/Stop Logic

---

# 🧪 **Phase 6 — Testing**

### 6.1 UI Testing
### 6.2 Hunger Bar Detection Testing
### 6.3 Auto-Feed Validation
### 6.4 Auto-Chop Validation

---

# 📦 **Phase 7 — Packaging / Polish**

### 7.1 Improve Visual Design
### 7.2 Add Settings Persistence
### 7.3 Add App Versioning
### 7.4 Add Release Metadata

---

# 🚀 **Phase 8 — Future Features (Optional)**

- Multi-Tool Automation  
- Global Hotkeys  
- Windows Support  
- Swift macOS Native Version  

---

# 🎉 Final Notes

This structured roadmap outlines every stage of the project and is ideal for use inside the /planning folder of the GitHub repository.
