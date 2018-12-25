import cv2
import numpy as np
import time



cv2.namedWindow("webcam")#, cv2.WND_PROP_FULLSCREEN)          
#cv2.setWindowProperty("webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()


i=0
start=time.time()
while True:
    ret, frame = cap.read()
    frame = frame[:500,:500]
    
    
    h,w=frame.shape[:2]
    
    
    y,x=np.mgrid[0:h,0:w]
    x=np.float32(x)
    y=np.float32(y)

    
    fps=i/(time.time()-start)
    
    #frame = frame[::160,::160]
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	
    gridx = x-w/2
    gridy = y-h/2
    
    r=np.hypot(gridx,gridy)
    theta=np.arctan2(gridy,gridx)
    
    thetap = theta+np.pi/4
    
    xp = r*np.cos(thetap)*2
    yp = r*np.sin(thetap)*2
	
    xp+=w/2
    yp+=h/2
    
    xp = np.float32(xp)
    yp = np.float32(yp)
    
    output=cv2.remap(frame, xp, yp, cv2.INTER_LINEAR)
    
    output[:,:,0] = 0
    
    cv2.imshow("webcam",frame)
    cv2.imshow("transformed",output)
    key=cv2.waitKey(1)
    if key==97:
        print(fps)
    i+=1
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()

