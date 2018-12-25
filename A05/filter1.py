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
    
    q = h/w
    
    rx = r/q*(((np.sin(theta))**2+(q*np.cos(theta))**2)**.5)
    ry = q*rx
    
    
    scale1 = ry/np.abs(gridy)
    scale2 = rx/np.abs(gridx)
    
    xp1 = scale1*gridx
    xp2 = scale2*gridx
    
    yp1 = scale1*gridy
    yp2 = scale2*gridy
    
    xp = xp1
    maskx = np.abs(xp2)<np.abs(xp1)
    
    yp = yp1
    masky = np.abs(yp2)<np.abs(yp1)
    
    xp[maskx] = xp2[maskx]
    yp[masky] = yp2[masky]
    
    #xp = gridx*ry/np.abs(gridy)
    #yp = ry*gridy/np.abs(gridy)
    
    
    xp+=w/2
    yp+=h/2
    
    xp = np.float32(xp)
    yp = np.float32(yp)
    
    #frame[:,:,:] = 0
    #for i in range(1,200,10):
    #    frame[i:h-1-i,i,0] = 255
    #    frame[i:h-1-i,w-1-i,0] = 255
    #    frame[i,i:w-1-i,1] = 255
    #    frame[h-1-i,i:w-1-i,2] = 255
    
    output=cv2.remap(frame, xp, yp, cv2.INTER_LINEAR)
    
    #output=theta
    
    #print(output)
    
    #output = np.maximum(output,frame)
    
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

