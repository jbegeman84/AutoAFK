
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

# 🧠 **High-Level Architecture Additions**

New modules to add under `src/`:
- `vision_core.py` – screenshot → OpenCV processing, basic helpers
- `avatar_detection.py` – recognize avatar facing/orientation
- `item_detection.py` – recognize stew item in hand
- `camera_control.py` – send key inputs to rotate/zoom camera in predictable ways
- `automation_profiles.py` – higher-level "scripts" like Auto-Feed 2.0, Auto-Stew-Collect

New dependency:
- `opencv-python` in `requirements.txt`

---

# 🔭 **Phase 6 — Computer Vision Foundations**

**Goal:** Add a small, testable vision layer that can reliably answer:  
"Is the avatar's hand + stew visible on screen right now?"

### 6.1 Add OpenCV Integration
- Update `requirements.txt` to include `opencv-python`.
- Create `vision_core.py`:
  - `capture_frame()` → returns a NumPy array (BGR) from `pyautogui.screenshot()`.
  - Helpers to convert between PIL and OpenCV if needed.
- Add a DEBUG toggle in the app to:
  - Save sample frames to disk (`debug_frames/frame_YYYYMMDD_HHMMSS.png`)
  - Optionally show a small "vision debug" window (even just writing detected status text in the GUI)

### 6.2 Template & Color-Based Detection Strategy
You probably don't need full "face recognition"; Roblox visuals are pretty stylized. Use simpler primitives:

**Template Matching:**
- Take a cropped screenshot of:
  - Avatar head/upper body (from a known good frontal view)
  - Stew-in-hand (from a known good view)
- Store these as PNGs in `assets/templates/`.

**`item_detection.py`:**
- `find_template(frame, template, threshold)` → returns best match location & score.
- `detect_stew_in_hand(frame)` -> `Optional[(x, y, w, h)]`.

**`avatar_detection.py`:**
- `detect_avatar_head(frame)` -> `Optional[(x, y, w, h)]` using another template or a color cluster.

**Success criteria for this phase:**
- Given a recorded test frame, a dev script can:
  - Load the frame
  - Answer True/False for "stew visible"
  - Answer True/False for "avatar head visible"
- No integration with the main app yet, just CLI tests and debug script.

### 6.3 Vision Calibration Wizard (Optional but very helpful)
- Add a menu item or button in the GUI: "Calibrate Vision for 99 Nights in the Forest".
- Flow:
  1. You manually put the camera in the desired front view.
  2. Click "Capture Avatar Template":
     - App takes screenshot.
     - You draw a small box over the avatar's head → template saved.
  3. Click "Capture Stew Template":
     - Select stew in hand, zoom appropriately.
     - App takes screenshot.
     - You draw a small box over stew-in-hand → template saved.
- Store these in `assets/templates/99nights_avatar.png`, `99nights_stew.png` and reference them in the detection modules.

---

# 🧭 **Phase 7 — Camera Orientation Detection & Control**

**Goal:** Make the app capable of getting the camera into a known configuration (e.g., front of avatar or top-down) so the stew is likely to be visible.

### 7.1 Camera Control Primitives
- Create `camera_control.py`:
  - Functions that send key presses / mouse drags to Roblox to adjust the camera. For example:
    - `rotate_left()`, `rotate_right()`
    - `zoom_in()`, `zoom_out()`
    - Maybe `reset_camera()` if the game has a known "reset camera" key.
  - These are wrappers around `pyautogui.keyDown/keyUp` or mouse drags.
  - Keep them small and deterministic: e.g., "rotate right by ~15°" is one specific keypress duration.

### 7.2 Orientation Recovery Logic
- In something like `avatar_detection.py` or a new `camera_state.py`, add:
  - `ensure_avatar_visible(app, state)` -> `bool`:
    - Pseudocode:
      ```
      for attempt in range(MAX_ATTEMPTS):
          frame = capture_frame()
          if avatar_detected(frame):
              return True
          
          # try a step of camera adjustment
          rotate_right_small()
          time.sleep(0.3)
      
      return False
      ```
- Later you can try a second strategy (top-down view) if front view fails:
  - Try a sequence: rotate a few times → zoom out slightly → re-check.

**Success criteria:**
- From a "bad" orientation, calling `ensure_avatar_visible()` will very often converge to a view where `avatar_detected(frame)` is True.
- You don't feed yet; we're just gaining control over camera orientation.

---

# 🍲 **Phase 8 — Stew-Aware Auto-Feed 2.0**

**Goal:** Replace "blind click at fixed coordinates" with a smarter, stew-aware feeding mode while keeping your existing macro mode as a backup.

### 8.1 Stew Detection Integration
- In a new module like `automation_profiles.py`, add:
  - `smart_feed_once(app, state)` -> `bool`:
    1. Ensure avatar is visible:
       - If not, call `ensure_avatar_visible()`.
    2. Capture frame.
    3. Call `detect_stew_in_hand(frame)`:
       - If stew not visible:
         - Press stew hotkey (stored in state).
         - Short delay.
         - Capture frame again → re-run stew detection.
    4. Once stew is detected:
       - You can either:
         - Use your existing feed trigger point (macro mode),
         - Or click closer to the detected stew bounding box center.
    5. Return True if feed action was attempted, False if conditions weren't met.

### 8.2 Integrate with Hunger Worker
- In your hunger workers (`worker_threads.py`):
  - Add a new mode: `feed_mode = "SMART_VISION"` in AppState.
  - If that mode is selected:
    - Use `smart_feed_once()` instead of `perform_feed()` or give user option:
      - "Use Vision-Based Feeding"
      - "Use Fixed-Point Macro Feeding"
- You now have three feeding modes:
  1. Timer + macro click
  2. Hunger monitor + macro click
  3. Hunger monitor + vision-based smart feed

### 8.3 Robustness / Safety
- To avoid "spam-clicking nothing" if detection fails:
  - If `smart_feed_once()` fails N times in a row:
    - Fallback to macro mode once
    - Or raise a visible error / speak a warning (e.g., using `say` on macOS).

---

# 🥘 **Phase 9 — Auto-Stew Collection from Crock Pot**

**Goal:** Add a feature where the app can periodically walk to the crock pot and collect stews, then return to the safe spot.  
This is more game-specific and fragile, so design it as a separate, opt-in profile that users configure and tweak.

### 9.1 Waypoint-Based Navigation
- Add to `automation_profiles.py`:
  - A simple "waypoint macro" system:
    - Record a sequence of keypresses (WASD) and mouse moves/drags to:
      - Walk from hideout → crock pot
      - Look at crock pot
      - Press E or click to collect stews
      - Walk back to hideout
    - Save this as a JSON script: `profiles/99nights_crockpot_route.json`
- Advanced version later: do some visual anchoring (e.g., detect campfire location or crock pot template to know you're aligned).

### 9.2 Crock Pot Interaction
- If the game shows stews on the top of the crock pot as distinct sprites:
  - Create a `detect_crockpot_stew(frame)` template.
  - Once at the crock pot:
    - Find stew sprites visually.
    - Click on them sequentially to pick up.
- If interaction is just one keypress (e.g. "E"), macros are enough.

### 9.3 Scheduling
- Add UI options:
  - "Auto-Stew Collection"
  - Run every X in-game days or every Y minutes.
  - Only run if not in immediate danger (optional future logic).
- Worker flow:
  - At certain intervals:
    - Pause feeding loop or mark "busy".
    - Run `run_crockpot_route()`.
    - Resume feeding.

---

# 🌱 **Phase 10 — Farm Plot / Resource Automation (Stretch Goals)**

This is definitely "advanced" and game-specific, so I'd treat it as a long-term stretch:

- Detect farm plots via template.
- Navigate using a grid of waypoints.
- Collect vegetables and deposit into storage or crock pot.
- Maybe detect "empty" vs "grown" crops via color/shape.

This phase would probably need:
- More robust CV (maybe using a mini classifier)
- More resilient navigation (game-specific pathing)

---

# 🧷 **Cross-Cutting Enhancements**

### A. Settings & Profiles
- Add a Game Profile concept:
  - "99 Nights in the Forest" profile defines:
    - Hotkeys
    - Template files
    - Default camera script
    - Stew slot, etc.
  - Save in a JSON config file to avoid hardcoding.

### B. Debug Tools
- **Vision Debug Panel:**
  - Show last hunger region image
  - Show overlay of stew detection bounding boxes
  - Show avatar detection bounding box
- **Logging:**
  - Write events like: "Avatar not found – rotating camera", "Stew not visible – pressing hotkey 3", etc.