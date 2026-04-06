def run_gesture():   
    import cv2
    import mediapipe as mp
    import pyautogui
    import time
    import math

    # Keep fail-safe ON (important)
    pyautogui.FAILSAFE = True

    # Screen size
    screen_w, screen_h = pyautogui.size()

    # Mediapipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    # Camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Finger tips
    tip_ids = [4, 8, 12, 16, 20]

    # Control parameters
    prev_x, prev_y = 0, 0
    prev_scroll_y = 0

    frame_reduction = 0.2  # 20% reduction on each side for better control
    smoothening = 2
    speed = 1.5   # slightly reduced to avoid corner jumps

    # Click control
    last_click_time = 0
    click_delay = 0.3
    last_screenshot_time = 0
    screenshot_delay = 2   # seconds

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        # Draw control box
        cv2.rectangle(frame, (int(frame_reduction), int(frame_reduction)),
                    (w - int(frame_reduction), h - int(frame_reduction)),
                    (255, 0, 255), 2)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                lm_list = []

                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # ---------------- FINGER DETECTION ----------------
                fingers = []

                # Thumb
                if lm_list[4][0] > lm_list[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers
                for i in range(1, 5):
                    if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i]-2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # ---------------- PAUSE (FIST) ----------------
                if fingers == [0,0,0,0,0]:
                    cv2.putText(frame, "PAUSED", (10, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
                    continue

                # ---------------- CURSOR MOVE ----------------
                if fingers == [0,1,0,0,0]:
                    x, y = lm_list[8]

                    # Limit area
                    x = min(max(x, frame_reduction), w - frame_reduction)
                    y = min(max(y, frame_reduction), h - frame_reduction)

                    # Convert to screen coords
                    screen_x = int((x - frame_reduction) * screen_w / (w - 2*frame_reduction) * speed)
                    screen_y = int((y - frame_reduction) * screen_h / (h - 2*frame_reduction) * speed)

                    # Prevent hitting corners (fail-safe fix)
                    screen_x = max(10, min(screen_w - 10, screen_x))
                    screen_y = max(10, min(screen_h - 10, screen_y))

                    # Smooth movement
                    curr_x = prev_x + (screen_x - prev_x) / smoothening
                    curr_y = prev_y + (screen_y - prev_y) / smoothening

                    pyautogui.moveTo(curr_x, curr_y)

                    prev_x, prev_y = curr_x, curr_y

                    cv2.putText(frame, "MOVE", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                # ---------------- CLICK (PINCH) ----------------
                x1, y1 = lm_list[4]
                x2, y2 = lm_list[8]

                distance = math.hypot(x2 - x1, y2 - y1)

                if distance < 20:  # Adjust threshold as needed
                    current_time = time.time()
                    if current_time - last_click_time > click_delay:
                        pyautogui.click()
                        last_click_time = current_time

                        cv2.putText(frame, "CLICK", (10, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                # ---------------- SCROLL ----------------

                current_time = time.time()

                # SCROLL DOWN (thumb only)
                if fingers == [1,0,0,0,0]:
                    if current_time - last_click_time > 0.2:
                        pyautogui.scroll(-40)
                        last_scroll_time = current_time

                # SCROLL UP (thumb + little finger)
                elif fingers == [1,0,0,0,1]:
                    if current_time - last_click_time > 0.2:
                        pyautogui.scroll(40)
                        last_scroll_time = current_time

                # ---------------- SCREENSHOT ----------------
                if fingers == [1,1,0,0,1]:
                    if current_time - last_screenshot_time > screenshot_delay:

                        filename = f"screenshot_{int(current_time)}.png"
                        pyautogui.screenshot(filename)

                        last_screenshot_time = current_time

                        cv2.putText(frame, "SCREENSHOT TAKEN", (10, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        cv2.imshow("Gesture Mouse Control", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()