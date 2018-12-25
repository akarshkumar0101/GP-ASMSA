import cv2
import numpy as np
import time


cv2.namedWindow("webcam")#, cv2.WND_PROP_FULLSCREEN)          
#cv2.setWindowProperty("webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
h,w=frame.shape[:2]
y,x=np.mgrid[0:h,0:w]
x=np.float32(x)
y=np.float32(y)
i=0
start=time.time()
while True:
    ret, frame = cap.read()
    fps=i/(time.time()-start)
    
    #xp=x+20*np.sin(y/w*2*np.pi*4+i/10.0)
    #yp=y+20*np.sin(x/w*2*np.pi*4+i/10.0)
    
    #r=np.hypot(x-w/2,y-h/2)
    #theta=np.arctan2(y-h/2,x-w/2)
    #thetap=theta+r/1000.0
    #xp=w/2+r*np.cos(thetap)
    #yp=h/2+r*np.sin(thetap)
    xp=np.sqrt(w*x)
    yp=np.sqrt(h*y)
    
    
    output=cv2.remap(frame, xp, yp, cv2.INTER_CUBIC)
    
    
    cv2.imshow("webcam",output)
    key=cv2.waitKey(1)
    if key==97:
        print(fps)
    i+=1
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()
