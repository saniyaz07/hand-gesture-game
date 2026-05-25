import cv2
import mediapipe as mp
import pyautogui
import time

# Safety
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

cap = cv2.VideoCapture(0)

left_pressed = False
right_pressed = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    left_hand = False
    right_hand = False

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label

            mp_draw.draw_landmarks(
                img, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            if label == "Left":
                left_hand = True
            elif label == "Right":
                right_hand = True

    # -------- KEY CONTROL --------
    if left_hand and not left_pressed:
        pyautogui.keyDown("left")
        left_pressed = True
    if not left_hand and left_pressed:
        pyautogui.keyUp("left")
        left_pressed = False

    if right_hand and not right_pressed:
        pyautogui.keyDown("right")
        right_pressed = True
    if not right_hand and right_pressed:
        pyautogui.keyUp("right")
        right_pressed = False

    cv2.putText(img, "LEFT hand = BRAKE (Left Arrow)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "RIGHT hand = ACCELERATE (Right Arrow)", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "Press Q to stop controller", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Hand Controller for Hill Climb", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release keys safely
pyautogui.keyUp("left")
pyautogui.keyUp("right")

cap.release()
cv2.destroyAllWindows()
