import cv2
import mediapipe as mp
import pyautogui
import time

SCREEN_W, SCREEN_H = pyautogui.size()
CLICK_DIST = 30
CLICK_DELAY = 0.3

class GestureMouse:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.draw = mp.solutions.drawing_utils
        self.last_click = 0
        print("Gesture Mouse Ready")
        print("Index finger = Move cursor")
        print("Pinch index = Left click")
        print("Pinch two fingers = Right click")
    
    def distance(self, p1, p2):
        return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2 + (p1.z-p2.z)**2)**0.5 * 1000
    
    def process(self, landmarks):
        thumb, index, middle = landmarks[4], landmarks[8], landmarks[12]
        pyautogui.moveTo(int(index.x * SCREEN_W), int(index.y * SCREEN_H), duration=0)
        if time.time() - self.last_click > CLICK_DELAY:
            if self.distance(thumb, index) < CLICK_DIST:
                pyautogui.click()
                self.last_click = time.time()
                print("Left click")
            elif self.distance(thumb, middle) < CLICK_DIST:
                pyautogui.rightClick()
                self.last_click = time.time()
                print("Right click")
    
    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    self.draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                    self.process(hand.landmark)
            cv2.imshow('Gesture Mouse (Press Q to quit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    GestureMouse().run()
