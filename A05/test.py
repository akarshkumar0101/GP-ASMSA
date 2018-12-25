import numpy as np
import cv2

ori=[]
for y in range (5):
	row = []
	for x in range (5):
		row.append(5*y+x)
	ori.append(row)
ori = np.array(ori)

y,x=np.mgrid[0:5,0:5]

xp=np.float32(x*1)
yp=np.float32(y*1)

img = cv2.remap(ori,xp,yp,cv2.INTER_LINEAR)
