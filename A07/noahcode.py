import cv2
import numpy as np
import time

cv2.namedWindow("webcam")  # , cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)


ret, frame = cap.read()
h, w = frame.shape[:2]
y, x = np.mgrid[0:h, 0:w]
x = np.float32(x)
y = np.float32(y)
i = 0
start = time.time()

while True:
    ret, frame = cap.read()
    fps = i / (time.time() - start)

    corners = cv2.goodFeaturesToTrack(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 100, 0.1, 15)
    corners = np.float32(corners)

    for item in corners:
        x, y = item[0]
        cv2.circle(frame, (x, y), 5, 255, -1)

    cv2.imshow("webcam", frame)
    key = cv2.waitKey(1)
    i += 1

cap.release()
cv2.destroyAllWindows()




def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result