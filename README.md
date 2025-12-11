# AFK Auto-Help

A macOS desktop utility that automates simple on-screen actions for Roblox gameplay, featuring hunger auto-feeding, timed clicking loops, and auto-chopping capabilities.

## Features Overview

- **Hunger Auto-Feed**: Automatically feeds your character based on hunger bar detection or timer intervals
- **Auto-Chop Tool**: Automated clicking for chopping actions with configurable rates and duration
- **Screen Region Selection**: Easy-to-use overlay for selecting screen regions and trigger points
- **Configurable Settings**: Customize thresholds, intervals, and automation parameters
- **Real-Time Status**: Monitor hunger levels and automation status in real-time

## Installation Instructions

### Prerequisites

- **Python 3.10+** (required)
- macOS 15.06+ (M1/M2/M3 compatible)

### Setup Steps

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd AutoAFK
   ```

2. Install dependencies:
   
   **For macOS 15.07+**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **For macOS 15.06** (if you get "requires macOS 15.07" error):
   ```bash
   pip install -r requirements-macos1506.txt
   ```
   
   This installs compatible versions of pyobjc that work with macOS 15.06.

3. Grant macOS permissions (required for screen interaction):
   - Open **System Settings** → **Privacy & Security**
   - Enable **Screen Recording** permission for Terminal (or your Python environment)
   - Enable **Input Monitoring** permission for Terminal (or your Python environment)
   
   **Note**: You may need to restart the application after granting permissions.

## macOS Permission Requirements

This application requires the following macOS permissions to function:

1. **Screen Recording**: Required to capture screenshots for hunger bar detection and screen region analysis
   - Location: System Settings → Privacy & Security → Screen Recording
   - Grant permission to Terminal or your Python interpreter

2. **Input Monitoring**: Required to simulate mouse clicks and keyboard input
   - Location: System Settings → Privacy & Security → Input Monitoring
   - Grant permission to Terminal or your Python interpreter

**Important**: Without these permissions, the application will not be able to interact with your screen or perform automated actions.

## Basic Usage Overview

1. Launch the application:
   ```bash
   python src/afk_auto_help.py
   ```

2. Configure your settings:
   - Select hunger bar region using the region selector
   - Set feed trigger coordinates
   - Configure timer intervals or hunger thresholds
   - Set up auto-chop parameters

3. Start automation:
   - Enable hunger auto-feed (timer or monitoring mode)
   - Enable auto-chop tool
   - Monitor status in the GUI

4. Stop automation:
   - Use the global **STOP ALL** button to halt all automation

## Contribution Instructions

Contributions are welcome! This project is open-source under the MIT License.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the development plan in `planning/development_plan.md`
- Write clear, documented code
- Test on macOS before submitting PRs
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
