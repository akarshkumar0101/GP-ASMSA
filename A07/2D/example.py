import cv2
import numpy as np
import random


#Specification
#Each corner will have a 5x5 tracker that will create two contours with a shared center.
#The outer contour will have the area of 25 units.
#The inner contours will differentiate the corners by having an area 3,5,7,or 9 units
#I will use a simple 16x16 grid to encode 32 bytes pre error correction.
#I will leave a 6 unit margin so the trackers doesn't touch the data.
#This brings the dimensions to 6+16+6=28.


img=np.zeros((28,28),dtype=np.uint8)

#make the part where there will be data white
img+=255
img[:6,:6]=0
img[-6:,:6]=0
img[:6,-6:]=0
img[-6:,-6:]=0
#store all these locations in the x and y arrays
#I will use this order to figure out how to put in data.
#This is 640bits=80bytes
x,y=np.where(img>0)

#Make the corners
img[:,:]=255
#box shape  area=9
img[:5,:5]=0
img[1:4,1:4]=255

#H shape area=7
img[-5:,:5]=0
img[-4:-1,1:4]=255
img[-3:-2,1:2]=0
img[-3:-2,3:4]=0

#S shape area=5
img[:5,-5:]=0
img[2:3,-4:-1]=255
img[1:2,-2:-1]=255
img[3:4,-4:-3]=255

#dash shape area=3
img[-5:,-5:]=0
img[-3:-2,-4:-1]=255

#cv2.imwrite("corners.png",img)

def getBits(s):
	from reedsolo import RSCodec
	rs=RSCodec(80-len(s))
	x=rs.encode(s)
	return np.unpackbits(np.uint8(list(x)))

#get an array of 0's and 1's
data=getBits(b"squirrel")
img=cv2.resize(img,(0,0),fx=40,fy=40,interpolation=cv2.INTER_NEAREST)
for i,j,k in zip(x,y,data):
	img[i*40+5:i*40+40-5,j*40+5:j*40+40-5]=(1-k)*255
	
cv2.imwrite("squirrel.png",img)
