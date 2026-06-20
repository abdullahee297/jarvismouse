import cv2
import time
import autopy
import math
import numpy as np 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = "hand_landmarker.task"),
    running_mode = VisionRunningMode.VIDEO,
    num_hands = 1
)

detector = HandLandmarker.create_from_options(options)

HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),                  # Thumb
        (0, 5), (5, 9), (9, 13), (13, 17), (17, 0),      # Wrist
        (5, 6), (6, 7), (7, 8),                          # Index
        (9, 10), (10, 11), (11, 12),                     # Middle
        (13, 14), (14, 15), (15, 16),                    # Ring
        (17, 18), (18, 19), (19, 20)                     # Pinky
    ]


cap = cv2.VideoCapture(0)
wcam = 640
hcam = 480
cap.set(3, wcam)
cap.set(4, hcam)
p_time = 0
wscn , hscn = autopy.screen.size()
frameR= 150
smoothness = 10
cLocX, cLocY = 0, 0
pLocX, pLocY = 0, 0
dragging = False
clicked = False


while True:
    success, img = cap.read()

    # img = cv2.flip(imgx, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(mp.ImageFormat.SRGB, rgb)

    time_stamp = int(time.time()*1000)

    result = detector.detect_for_video(mp_image, time_stamp)


    finger_count = 0
    finger = []

    if result.hand_landmarks:
        for hands in result.hand_landmarks:
            h, w, _ = img.shape
            lm_list = []
            x_list = []
            y_list = []

            for lm in hands:
                lm_list.append((int(lm.x*w), int(lm.y*h)))
                x_list.append(int(lm.x*w))
                y_list.append(int(lm.y*h))

            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0))


            # Draw connections
            for start, end in HAND_CONNECTIONS:
                    cv2.line(img, lm_list[start], lm_list[end], (0, 255, 0), 2)

            # Draw landmarks
            for x, y in lm_list:
                cv2.circle(img, (x, y), 4, (0, 0, 255), cv2.FILLED)

            x1, y1 = lm_list[4][0], lm_list[4][1]
            x2, y2 = lm_list[8][0], lm_list[8][1]
            x3, y3 = lm_list[12][0], lm_list[12][1]

            x5 = np.interp(x2, (frameR, wcam-frameR), (0, wscn))
            y5 = np.interp(y2, (frameR, hcam-frameR), (0, hscn))

            # For click/select
            x4, y4 = (x3+x2)//2, (y3+y2)//2

            # Center point of the line for dragging
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


            cv2.circle(img, 
                       (x1, y1),
                       10,
                       (255,0,255),
                       cv2.FILLED
                       )
            
            cv2.circle(img, 
                       (x2, y2),
                       10,
                       (255,0,255),
                       cv2.FILLED
                       )
            
            cv2.line(img,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 255),
                    5
                    )
            
            cv2.circle(img,
                        (cx, cy),
                        10,
                        (100, 160, 50),
                        cv2.FILLED
                        )
            
            cv2.rectangle(img,
                          (x2, y2),
                          (x3, y3),
                          (0, 255, 0),
                          2
                          )

            if lm_list[4][0] < lm_list[4][1]:
                finger_count += 1
                finger.append(1)

            else:
                finger.append(0)

            tips = [8,12, 16, 20]
            pips = [6,10, 14, 18]

            for tip, pip in zip(tips, pips):
                if lm_list[tip][1] < lm_list[pip][1]:
                    finger_count += 1
                    finger.append(1)

                else:
                    finger.append(0)


            if finger[1] and finger[2] and finger[3]:
                autopy.mouse.click(autopy.mouse.Button.RIGHT)


            if finger[1] and finger[2] and not finger[3]:
                print("Left Click")
                cv2.circle(img, (x4, y4), 15, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "Left Click", (20, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
                length = math.hypot(x3 - x2, y3 - y2)
                print(length)
                if length < 20:
                    autopy.mouse.click()

            if finger[1] and not finger[2]:
                print("Move")
                cv2.rectangle(img, (frameR, frameR),
                             (wcam-frameR, hcam-frameR),
                             (255, 0, 255), 2)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Move the curser", (20, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
                
                cLocX = pLocX + (x5 - pLocX) / smoothness
                cLocY = pLocY + (y5 - pLocY) / smoothness
        
                autopy.mouse.move(wscn-cLocX, cLocY)
                pLocX, pLocY = cLocX, cLocY


            draglength = math.hypot(x2 - x1, y2 - y1)
            print(draglength)

            if draglength < 15:
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

                if not dragging:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)   # Press and hold
                    dragging = True

                cv2.putText(img, "Dragging", (20, 120),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

            else:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                if dragging:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)  # Release
                    dragging = False

                cv2.putText(img, "Released", (20, 120),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 0), 2)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(img,
                f'FPS: {int(fps)}',
                (20, 40),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 0, 0),
                3)



    cv2.imshow("Jarvis Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break  


cap.release()
cv2.destroyAllWindows()
