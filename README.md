# Gesture Controlled Virtual Mouse

A gesture and voice-controlled virtual mouse using Computer Vision and Speech Recognition.

## Features

- **🖱️ Complete Mouse Control**:
  - **Cursor Movement**: Raise index and middle fingers.
  - **Left Click**: Lower index finger while middle finger is up.
  - **Right Click**: Lower middle finger while index finger is up.
  - **Double Click**: Perform two quick left clicks.
- **🎤 Voice Commands**:
  - "left click", "right click", "double click"
  - "scroll up", "scroll down"
- **📹 Real-time Processing**:
  - Live webcam feed processing.
  - Smooth cursor movement with configurable smoothing.
  - Visual feedback with hand landmarks and current mode display.
- **🎯 Easy to Use**:
  - No additional hardware required (just a webcam and microphone).
  - Simple gesture and voice vocabulary.

## Technology Stack

- **OpenCV**: For camera feed and image processing.
- **MediaPipe**: For hand tracking and landmark detection.
- **PyAutoGUI**: For programmatic mouse control.
- **SpeechRecognition**: For voice command processing.
- **PyAudio**: Required by SpeechRecognition to access the microphone.

## Installation

It is highly recommended to use a Python virtual environment to avoid conflicts with your global packages.

1.  **Clone or Download** this repository.

2.  **Create and Activate a Virtual Environment**:

    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```
    Or install manually:
    ```bash
    pip install opencv-python mediapipe pyautogui SpeechRecognition pyaudio
    ```

## Usage

1.  **Activate the virtual environment** if it's not already active:
    ```bash
    .\venv\Scripts\activate
    ```

2.  **Run the Application**:
    ```bash
    python gesture_mouse.py
    ```
2.  **Position Your Hand** in front of the camera. The cursor will only move when your index finger is inside the designated on-screen rectangle.
3.  **Use Gestures and Voice Commands**:

    | Action | Gesture / Voice Command |
    | :--- | :--- |
    | **Move Cursor** | Raise both index and middle fingers. |
    | **Left Click** | Lower index finger while middle finger is up. |
    | **Right Click** | Lower middle finger while index finger is up. |
    | **Double Click** | Perform two quick left clicks. |
    | **Voice Commands** | Say "left click", "right click", "double click", "scroll up", "scroll down". |
    | **Exit** | Press the 'q' key on the keyboard. |

## How It Works

1.  **Hand Detection**: The system uses MediaPipe to detect and track 21 key points on a single hand in real-time.
2.  **Gesture Recognition**: The application analyzes the state of the index and middle fingers (up or down) to recognize gestures.
    -   **Finger State**: It checks if a finger is "up" by comparing the vertical position of its tip to its middle joint (PIP).
    -   **Movement**: When both index and middle fingers are up, the position of the index fingertip is mapped to the screen to move the cursor. Movement is smoothed to reduce jitter.
    -   **Clicks**: A click is triggered when one finger goes down while the other remains up.
3.  **Voice Recognition**: A separate thread listens for voice commands using the `SpeechRecognition` library. It can perform clicks and scrolling, complementing the gesture controls.
4.  **Mouse Control**: Recognized gestures and voice commands are translated into mouse actions using `PyAutoGUI`.

## Configuration

You can modify these parameters at the top of `gesture_mouse.py`:

```python
# Camera and smoothing settings
CAM_WIDTH, CAM_HEIGHT = 640, 480
SMOOTHING = 7
MOVE_REGION = (0.2, 0.8, 0.2, 0.8) # Active area for cursor movement
DOUBLE_CLICK_INTERVAL = 0.4
```

## Troubleshooting

-   **Microphone/Speech Issues**: Ensure you have `PyAudio` installed. If you get a "Microphone not available" error, check that your mic is connected and not in use by another application.
-   **Camera Issues**: Ensure your camera is connected and working. The script uses the default camera (index 0).
-   **Gesture Recognition**:
    -   Use in a well-lit environment.
    -   Keep your hand clearly visible in the camera frame.
    -   Make distinct finger movements.

## Code Structure

The program is a single script (`gesture_mouse.py`) with the following components:
-   **Configuration**: Global variables for tuning performance.
-   **Helper Functions**: `finger_is_up`, `calc_angle_between_fingers`.
-   **State Variables**: To track previous finger states for gesture detection.
-   **`speech_listener()` function**: Runs in a background thread to handle voice commands.
-   **Main Loop**:
    -   Initializes MediaPipe, PyAutoGUI, and OpenCV.
    -   Captures video frames.
    -   Processes hand landmarks.
    -   Detects gestures and moves the mouse.
    -   Displays visual feedback on the screen.

## Limitations

-   Single-hand detection by default.
-   Requires good lighting and a clear background for best performance.
-   Voice recognition requires an internet connection for the default Google Web Speech API.

## References

-  https://ijarsct.co.in/Paper10833.pdf

---

**Happy Gesture Computing! 🖱️✋**
