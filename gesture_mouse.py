import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading

try:
    import speech_recognition as sr
    import pyaudio
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

# === Config ===
CAM_WIDTH, CAM_HEIGHT = 640, 480
SMOOTHING = 7
MOVE_REGION = (0.2, 0.8, 0.2, 0.8)
DOUBLE_CLICK_INTERVAL = 0.4

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
    return landmarks[tip_id].y < landmarks[pip_id].y

def calc_angle_between_fingers(landmarks, a_idx, b_idx, base_idx):
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
    return math.degrees(math.acos(cosv))

# State variables
prev_index_up = None
prev_middle_up = None
smooth_x = screen_w // 2
smooth_y = screen_h // 2
last_click_time = 0

def find_working_microphone():
    """Auto-detect working microphone by testing each one"""
    if not SPEECH_AVAILABLE:
        return None
    
    try:
        mics = sr.Microphone.list_microphone_names()
        r = sr.Recognizer()
        
        # Try to find a microphone with reasonable input levels
        for i in range(len(mics)):
            try:
                with sr.Microphone(device_index=i) as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    if r.energy_threshold > 50:  # If it picks up reasonable audio levels
                        print(f"[Speech] Auto-selected microphone [{i}]: {mics[i]}")
                        return i
            except:
                continue
        
        # If no good mic found, try default
        print("[Speech] Using default microphone")
        return None
    except:
        return None

def speech_listener():
    """Voice command recognition thread"""
    if not SPEECH_AVAILABLE:
        print("[Voice] Speech recognition not available. Install: pip install SpeechRecognition pyaudio")
        return
    
    mic_index = find_working_microphone()
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    
    try:
        mic = sr.Microphone(device_index=mic_index) if mic_index else sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print(f"[Voice] Ready! Say: 'click', 'right click', 'double click', 'scroll up/down'")
        
        while True:
            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                
                text = recognizer.recognize_google(audio, language='en-US').lower()
                
                # Execute commands
                if 'right' in text and 'click' in text:
                    pyautogui.click(button='right')
                elif 'double' in text:
                    pyautogui.doubleClick()
                elif 'click' in text or 'left' in text:
                    pyautogui.click()
                elif 'scroll' in text and 'up' in text:
                    pyautogui.scroll(500)
                elif 'scroll' in text and 'down' in text:
                    pyautogui.scroll(-500)
                    
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                time.sleep(1)
            except Exception:
                break
                
    except Exception as e:
        print(f"[Voice] Error: {e}")

# Start voice recognition in background
if SPEECH_AVAILABLE:
    threading.Thread(target=speech_listener, daemon=True).start()
    time.sleep(0.5)

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

            # Use wrist (landmark 0) for cursor position tracking instead of index finger
            # This way, lowering index finger won't move cursor down
            wrist_x = int(lm[0].x * w)
            wrist_y = int(lm[0].y * h)

            # Map active region to full screen coords
            # Restrict motions to MOVE_REGION then map linearly to screen
            if (x_min <= wrist_x <= x_max) and (y_min <= wrist_y <= y_max):
                # normalize within region
                nx = (wrist_x - x_min) / (x_max - x_min)
                ny = (wrist_y - y_min) / (y_max - y_min)
                target_x = screen_w * nx
                target_y = screen_h * ny

                # smoothing
                smooth_x = smooth_x + (target_x - smooth_x) / SMOOTHING
                smooth_y = smooth_y + (target_y - smooth_y) / SMOOTHING

            # Move cursor when both fingers are up
            if index_up and middle_up:
                pyautogui.moveTo(smooth_x, smooth_y, duration=0)
                cv2.putText(frame, "Moving", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            
            # Detect gestures (skip first frame)
            if prev_index_up is not None:
                # Left click: index down, middle up
                if (prev_index_up and not index_up) and middle_up:
                    now = time.time()
                    if now - last_click_time < DOUBLE_CLICK_INTERVAL:
                        pyautogui.doubleClick()
                    else:
                        pyautogui.click()
                    last_click_time = now
                
                # Right click: middle down, index up
                if index_up and (prev_middle_up and not middle_up):
                    pyautogui.click(button='right')

            # Visual feedback
            status = f"Index: {'UP' if index_up else 'DN'} | Middle: {'UP' if middle_up else 'DN'}"
            cv2.putText(frame, status, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            cv2.circle(frame, (wrist_x, wrist_y), 6, (0, 255, 255), -1)

            # Update states
            prev_index_up = index_up
            prev_middle_up = middle_up
        else:
            cv2.putText(frame, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # Show frame
        cv2.imshow("Gesture Mouse - Press 'q' to quit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Stopped.")
