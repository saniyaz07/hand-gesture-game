import cv2
import mediapipe as mp
import pyautogui
import math
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = 0, 0

def finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark

        fingers = [
            finger_up(lm, 8, 6),   # index
            finger_up(lm, 12, 10), # middle
            finger_up(lm, 16, 14), # ring
            finger_up(lm, 20, 18)  # pinky
        ]

        index_x = int(lm[8].x * screen_w)
        index_y = int(lm[8].y * screen_h)

        # 👉 Mouse movement (Index finger)
        if fingers == [True, False, False, False]:
            pyautogui.moveTo(index_x, index_y, duration=0.1)

        # ✌️ Left click
        if fingers == [True, True, False, False]:
            pyautogui.click()
            time.sleep(0.3)

        # 🤟 Right click
        if fingers == [True, True, True, False]:
            pyautogui.rightClick()
            time.sleep(0.3)

        # ✊ Play / Pause (Fist)
        if fingers == [False, False, False, False]:
            pyautogui.press("playpause")
            time.sleep(0.5)

        # ✋ Show Desktop
        if fingers == [True, True, True, True]:
            pyautogui.hotkey("win", "d")
            time.sleep(0.5)

        # 👍 Volume up
        if lm[4].y < lm[3].y:
            pyautogui.press("volumeup")

        # 👎 Volume down
        if lm[4].y > lm[3].y:
            pyautogui.press("volumedown")

    cv2.imshow("Hand Laptop Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
