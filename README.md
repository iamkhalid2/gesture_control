# Gesture Controlled Virtual Mouse

A gesture and voice-controlled virtual mouse using Computer Vision and Speech Recognition.

## Features

🖱️ **Mouse Control**
- Move cursor by raising both index and middle fingers
- Left click by lowering index finger (middle stays up)
- Right click by lowering middle finger (index stays up)
- Double click with two quick left clicks

🎤 **Voice Commands**
- "click" or "left click"
- "right click"
- "double click"
- "scroll up" / "scroll down"

📹 **Real-time Processing**
- Live webcam feed with hand tracking
- Smooth cursor movement
- Visual feedback with hand landmarks

## Technology Stack

- **OpenCV**: Camera feed and image processing
- **MediaPipe**: Hand tracking and landmark detection
- **PyAutoGUI**: Mouse control
- **SpeechRecognition**: Voice command processing
- **PyAudio**: Microphone access

## Installation

**Using Virtual Environment (Recommended):**

```bash
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Activate virtual environment** (if using):
   ```bash
   .\venv\Scripts\activate
   ```

2. **Run the application**:
   ```bash
   python gesture_mouse.py
   ```

3. **Gestures**:
   - **Move**: Raise both index and middle fingers, move your wrist
   - **Left Click**: Lower index finger while middle is up
   - **Right Click**: Lower middle finger while index is up

4. **Exit**: Press 'q' key

## How It Works

1. **Hand Detection**: MediaPipe detects 21 hand landmarks in real-time
2. **Cursor Tracking**: Wrist position controls cursor (not fingertip), preventing unwanted movement during clicks
3. **Gesture Recognition**: Finger up/down states trigger clicks
4. **Voice Recognition**: Auto-detects working microphone and listens for commands
5. **Smoothing**: Cursor movement is smoothed to reduce jitter

## Configuration

Edit these values in `gesture_mouse.py`:

```python
CAM_WIDTH, CAM_HEIGHT = 640, 480    # Camera resolution
SMOOTHING = 7                        # Cursor smoothing (higher = smoother)
MOVE_REGION = (0.2, 0.8, 0.2, 0.8)  # Active tracking area
DOUBLE_CLICK_INTERVAL = 0.4          # Max time between clicks for double-click
```

## Troubleshooting

### Voice Commands Not Working?

The application **automatically detects** the working microphone. If it fails:

1. Check Windows Sound Settings (Right-click speaker icon → Sounds → Recording)
2. Ensure microphone is enabled and not muted
3. Set as default recording device
4. Increase microphone volume

### Camera Issues

- Ensure camera is connected and not used by other applications
- Script uses default camera (index 0)

### Gesture Recognition Issues

- Use good lighting
- Keep hand clearly visible in the rectangle
- Make distinct finger movements

## Code Structure

The code is ~150 lines, organized as:
- **Config**: Global settings
- **Helper Functions**: Finger detection, angle calculation
- **Auto Microphone Detection**: Finds working microphone automatically
- **Voice Recognition Thread**: Runs in background
- **Main Loop**: Hand detection and gesture recognition

## References

-  https://ijarsct.co.in/Paper10833.pdf

---

**Happy Gesture Computing! 🖱️✋**