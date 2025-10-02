# Gesture Controlled Virtual Mouse# Gesture Controlled Virtual Mouse



Ultra-minimal gesture mouse control system.A simple and easy-to-understand implementation of a gesture-controlled virtual mouse using Computer Vision and Machine Learning, based on the Aurora Report methodology.



## Quick Start## Features



1. **Install dependencies:**🖱️ **Complete Mouse Control**

   ```bash- Cursor movement with index finger

   pip install -r requirements.txt- Left click with thumb + index pinch

   ```- Right click with thumb + middle pinch  

- Scrolling with pinch + vertical movement

2. **Run:**- Exit with open palm gesture

   ```bash

   python gesture_mouse.py📹 **Real-time Processing**

   ```- Live webcam feed processing

- Smooth cursor movement

## How to Use- Low latency gesture recognition

- Visual feedback with hand landmarks

- **Move cursor:** Point with your index finger

- **Left click:** Pinch thumb and index finger together🎯 **Easy to Use**

- **Right click:** Pinch thumb and middle finger together- No additional hardware required

- **Quit:** Press 'Q' key- Works with any standard webcam

- Simple gesture vocabulary

## Requirements- User-friendly interface



- Python 3.7+## Technology Stack

- Webcam

- Windows/Mac/Linux- **OpenCV**: Computer vision and image processing

- **MediaPipe**: Hand tracking and landmark detection

## Code Overview- **PyAutoGUI**: Mouse control and automation

- **NumPy**: Mathematical operations

The entire program is **~70 lines** of clean, efficient code:- **Python 3.7+**: Core programming language

- Uses MediaPipe for hand tracking

- Detects finger positions and pinch gestures## Installation

- Maps finger position to screen coordinates

- Simple distance calculation for click detection1. **Clone or Download** this repository

2. **Install Required Packages**:

That's it! No complex configuration needed.   ```bash

   pip install opencv-python mediapipe pyautogui numpy
   ```

## Usage

1. **Run the Application**:
   ```bash
   python gesture_mouse.py
   ```

2. **Position Your Hand** in front of the camera (about 1-2 feet away)

3. **Use These Gestures**:

   | Gesture | Action | Description |
   |---------|--------|-------------|
   | ☝️ Index finger only | Move Cursor | Point with your index finger to control cursor |
   | 👌 Thumb + Index pinch | Left Click | Bring thumb and index finger close together |
   | 🤏 Thumb + Middle pinch | Right Click | Bring thumb and middle finger close together |
   | 📜 Pinch + Move up/down | Scroll | Make pinch gesture and move hand vertically |
   | ✋ All fingers extended | Exit | Show open palm to exit application |

4. **Exit**: Press 'q' key or show open palm gesture

## How It Works

### 1. Hand Detection
The system uses MediaPipe to detect and track hand landmarks in real-time. It identifies 21 key points on the hand including fingertips and joints.

### 2. Gesture Recognition
The application analyzes finger positions to determine gestures:
- **Finger Extension Detection**: Compares tip and joint positions
- **Pinch Detection**: Calculates distance between thumb and other fingertips
- **Movement Tracking**: Monitors position changes for scrolling

### 3. Mouse Control
Recognized gestures are translated to mouse actions:
- **Cursor Movement**: Index finger position mapped to screen coordinates
- **Clicking**: Pinch gestures trigger left/right clicks with debouncing
- **Scrolling**: Vertical hand movement during pinch creates scroll events

### 4. Smoothing and Stability
- **Movement Smoothing**: Reduces cursor jitter with interpolation
- **Click Debouncing**: Prevents multiple rapid clicks
- **Gesture Filtering**: Ensures stable gesture recognition

## Configuration

You can modify these parameters in the code:

```python
# Gesture sensitivity
self.click_threshold = 40        # Distance for pinch detection
self.scroll_threshold = 30       # Movement for scroll detection
self.smoothing_factor = 0.7      # Cursor smoothing (0-1)
self.click_delay = 0.3          # Delay between clicks (seconds)

# Detection confidence
min_detection_confidence=0.7     # Hand detection threshold
min_tracking_confidence=0.7      # Hand tracking threshold
```

## System Requirements

- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **Python**: 3.7 or higher
- **Camera**: Any USB webcam or built-in camera
- **RAM**: 4GB minimum, 8GB recommended
- **Processor**: Any modern CPU (no GPU required)

## Troubleshooting

### Camera Issues
- Ensure camera is connected and not used by other applications
- Check camera permissions in your OS settings
- Try different camera indices if you have multiple cameras

### Gesture Recognition Issues
- Ensure good lighting conditions
- Keep hand clearly visible in camera frame
- Maintain steady hand movements
- Adjust detection confidence if needed

### Performance Issues
- Close other camera applications
- Reduce camera resolution if needed
- Ensure adequate system resources

## Code Structure

```
gesture_mouse.py
├── GestureMouseController (Main Class)
│   ├── __init__()              # Initialize MediaPipe and settings
│   ├── get_distance()          # Calculate distance between points
│   ├── is_finger_extended()    # Check if finger is extended
│   ├── detect_gesture()        # Main gesture recognition logic
│   ├── perform_action()        # Execute mouse actions
│   ├── draw_landmarks_and_info() # Visual feedback
│   └── run()                   # Main execution loop
└── main()                      # Entry point
```

## Customization

### Adding New Gestures
1. Modify the `detect_gesture()` method
2. Add new gesture recognition logic
3. Update `perform_action()` to handle new gestures
4. Add visual feedback if needed

### Changing Sensitivity
Adjust threshold values for different sensitivity levels:
- Lower values = more sensitive
- Higher values = less sensitive

### Multi-hand Support
Modify MediaPipe settings:
```python
self.hands = self.mp_hands.Hands(
    max_num_hands=2,  # Change from 1 to 2
    ...
)
```

## Safety Features

- **Failsafe Disabled**: PyAutoGUI failsafe is disabled for smooth operation
- **Click Debouncing**: Prevents accidental multiple clicks
- **Smooth Movement**: Reduces sudden cursor jumps
- **Multiple Exit Options**: 'q' key or palm gesture to exit

## Limitations

- Requires good lighting conditions
- Single hand detection by default
- May need calibration for different users
- Performance depends on camera quality

## Future Enhancements

- Multi-hand gesture support
- Calibration interface for personalization
- Additional gesture commands
- Voice command integration
- Settings configuration file

## Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Based on methodology from Aurora Research Report
- MediaPipe by Google Research
- OpenCV Community
- PyAutoGUI Library

---

**Happy Gesture Computing! 🖱️✋**
