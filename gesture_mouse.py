"""
Gesture Controlled Virtual Mouse
Implementation following the methodology of the uploaded report (MediaPipe + OpenCV + SpeechRecognition + pyautogui/pynput).
Finger ids (MediaPipe Hands):
 - 8 : index finger tip
 - 6 : index finger PIP (used to test if index is up)
 - 12: middle finger tip
 - 10: middle finger PIP
Refer to report for method description. (See file attached in conversation.)
"""

import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading
import speech_recognition as sr

# === Config ===
CAM_WIDTH, CAM_HEIGHT = 640, 480          # camera capture resolution
SMOOTHING = 7                             # higher -> smoother cursor
MOVE_REGION = (0.2, 0.8, 0.2, 0.8)       # normalized active region (x_min, x_max, y_min, y_max)
CLICK_DISTANCE_THRESHOLD = 40            # px threshold (on camera frame) to detect pinch for click if used
DOUBLE_CLICK_INTERVAL = 0.4              # seconds

# Initialize pyautogui
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

# Helper functions
def finger_is_up(landmarks, tip_id, pip_id):
    """
    Return True if the finger's tip Y is above (smaller) than the pip Y -> finger up.
    landmarks: list of normalized landmarks from MediaPipe
    """
    return landmarks[tip_id].y < landmarks[pip_id].y

def calc_angle_between_fingers(landmarks, a_idx, b_idx, base_idx):
    """
    Compute angle (degrees) between vector(base->a) and vector(base->b)
    """
    ax = landmarks[a_idx].x - landmarks[base_idx].x
    ay = landmarks[a_idx].y - landmarks[base_idx].y
    bx = landmarks[b_idx].x - landmarks[base_idx].x
    by = landmarks[b_idx].y - landmarks[base_idx].y
    dot = ax*bx + ay*by
    mag_a = math.hypot(ax, ay)
    mag_b = math.hypot(bx, by)
    if mag_a * mag_b == 0:
        return 0.0
    cosv = max(min(dot / (mag_a*mag_b), 1.0), -1.0)
    angle = math.degrees(math.acos(cosv))
    return angle

# State variables
prev_index_up = False
prev_middle_up = False
prev_time_left_click = 0
smooth_x = 0
smooth_y = 0
last_click_time = 0

# Speech recognition thread (simple commands)
def speech_listener():
    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone not available or pyaudio not installed:", e)
        return

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)

    print("[Speech] Ready for voice commands (say: left click, right click, double click, scroll up, scroll down)")
    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=2.5)
            cmd = recognizer.recognize_google(audio).lower()
            print("[Speech] Heard:", cmd)
            if "left click" in cmd or "click" == cmd.strip():
                pyautogui.click()
            elif "double click" in cmd or "double" in cmd:
                pyautogui.doubleClick()
            elif "right click" in cmd or "right" in cmd:
                pyautogui.click(button='right')
            elif "scroll up" in cmd or "scroll" in cmd and "up" in cmd:
                pyautogui.scroll(500)
            elif "scroll down" in cmd:
                pyautogui.scroll(-500)
            elif "exit mouse" in cmd or "stop" in cmd:
                print("[Speech] Exiting speech listener")
                break
        except sr.UnknownValueError:
            # no speech recognized
            pass
        except Exception as e:
            print("[Speech] error:", e)
            time.sleep(0.5)

# Start speech listener in daemon thread
speech_thread = threading.Thread(target=speech_listener, daemon=True)
speech_thread.start()

# OpenCV capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

print("Starting gesture-controlled cursor. Press 'q' to quit.")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # flip horizontally for mirror view
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        h, w, _ = frame.shape

        # draw active region rectangle for user guidance
        x_min = int(MOVE_REGION[0] * w)
        x_max = int(MOVE_REGION[1] * w)
        y_min = int(MOVE_REGION[2] * h)
        y_max = int(MOVE_REGION[3] * h)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (200,200,200), 1)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            lm = hand_landmarks.landmark

            # draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # finger states
            index_up = finger_is_up(lm, 8, 6)
            middle_up = finger_is_up(lm, 12, 10)

            # compute angle between index and middle (using base = wrist (0))
            angle = calc_angle_between_fingers(lm, 8, 12, 0)

            # get index tip position in pixel coordinates
            idx_x = int(lm[8].x * w)
            idx_y = int(lm[8].y * h)

            # Map active region to full screen coords
            # Restrict motions to MOVE_REGION then map linearly to screen
            if (x_min <= idx_x <= x_max) and (y_min <= idx_y <= y_max):
                # normalize within region
                nx = (idx_x - x_min) / (x_max - x_min)
                ny = (idx_y - y_min) / (y_max - y_min)
                target_x = screen_w * nx
                target_y = screen_h * ny

                # smoothing
                smooth_x = smooth_x + (target_x - smooth_x) / SMOOTHING
                smooth_y = smooth_y + (target_y - smooth_y) / SMOOTHING

            # Move cursor when both index and middle fingers are up (per report)
            if index_up and middle_up:
                pyautogui.moveTo(smooth_x, smooth_y, duration=0)  # instant movement
                cv2.putText(frame, "Mode: Move", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            else:
                # If index goes from up -> down while middle remains up: left click (per report)
                if (prev_index_up and not index_up) and middle_up:
                    # optional: check angle > 33.5 deg as in report
                    if angle > 33.5:
                        # debounce double click
                        now = time.time()
                        if now - last_click_time < DOUBLE_CLICK_INTERVAL:
                            pyautogui.doubleClick()
                            cv2.putText(frame, "Double Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,128,255), 2)
                        else:
                            pyautogui.click()
                            cv2.putText(frame, "Left Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,128,255), 2)
                        last_click_time = now
                # Right click gesture (index up and middle down) - implement: index up, middle down -> right click
                if index_up and (prev_middle_up and not middle_up):
                    pyautogui.click(button='right')
                    cv2.putText(frame, "Right Click", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            # update previous
            prev_index_up = index_up
            prev_middle_up = middle_up

            # show debug info
            cv2.circle(frame, (idx_x, idx_y), 6, (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, f"Angle:{angle:.1f}", (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

        # show
        cv2.imshow("Virtual Mouse (press q to quit)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Stopped.")
