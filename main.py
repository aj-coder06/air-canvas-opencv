import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Dark colors
colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255)]
color_index = 0

smooth_x, smooth_y = 0, 0
alpha = 0.5  # smoothing factor (0.3–0.7 works well)

canvas = None
prev_x, prev_y = 0, 0

cap = cv2.VideoCapture(0)

# Fullscreen
cv2.namedWindow("Air Canvas", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Gesture tracking
prev_fist = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    h, w, _ = frame.shape

    # Show current color (top-right)
    center = (w - 60, 60)  # center of circle (top-right)
    radius = 50

    cv2.circle(frame, center, radius, colors[color_index], -1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            # Coordinates
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)

            # Finger states
            index = lm[8].y < lm[6].y
            middle = lm[12].y < lm[10].y
            ring = lm[16].y < lm[14].y
            pinky = lm[20].y < lm[18].y

            fingers_up = [index, middle, ring, pinky]

            # Detect fist (all down)
            fist = not any(fingers_up)

            # Detect all fingers up
            all_up = all(fingers_up)

            # Color change (fist → open)
            if prev_fist and all_up:
                color_index = (color_index + 1) % len(colors)

            prev_fist = fist

            # DRAW
            if index and not middle and not ring and not pinky:

                # First frame of drawing → just initialize
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y
                    smooth_x, smooth_y = x, y
                    continue

                # Apply smoothing
                smooth_x = int(alpha * x + (1 - alpha) * prev_x)
                smooth_y = int(alpha * y + (1 - alpha) * prev_y)

                # Distance between points
                distance = int(np.hypot(smooth_x - prev_x, smooth_y - prev_y))

                # Avoid weird jumps
                if distance > 50:
                    prev_x, prev_y = smooth_x, smooth_y
                    continue

                # Interpolation
                for i in range(1, distance):
                    interp_x = int(prev_x + (smooth_x - prev_x) * i / distance)
                    interp_y = int(prev_y + (smooth_y - prev_y) * i / distance)
                    cv2.circle(canvas, (interp_x, interp_y), 4, colors[color_index], -1)

                prev_x, prev_y = smooth_x, smooth_y

            # ERASE
            elif index and middle and not ring and not pinky:
                cv2.circle(canvas, (x, y), 25, (0,0,0), -1)
                prev_x, prev_y = 0, 0

            # STOP (all fingers up or others)
            else:
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Merge canvas + frame
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray_canvas, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Air Canvas", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = None

cap.release()
cv2.destroyAllWindows()