import cv2
import numpy as np

h = 500
w = 500
img=np.ones((h,w,3),dtype = np.uint8)

img[:,:,:] = 0

y,x=np.mgrid[0:h,0:w]
gridx = x-w/2
gridy = y-h/2

r = np.hypot(gridx,gridy)
theta=np.arctan2(y-h/2,x-w/2)
theta-=np.min(theta)
theta/=np.max(theta)
theta*=255.9

img = theta

img = np.uint8(img)

img_color = cv2.applyColorMap(img, cv2.COLORMAP_JET)
img = img_color


perr = r/np.max(r)
img[:,:,0]=img[:,:,0]*perr[:,:]
img[:,:,1]=img[:,:,1]*perr[:,:]
img[:,:,2]=img[:,:,2]*perr[:,:]
img= np.uint8(img)




cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
