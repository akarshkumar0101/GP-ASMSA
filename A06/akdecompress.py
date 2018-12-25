import numpy as np
import cv2
import struct
from BitWriter import BitFile


print("compressed file:")
f=BitFile(input(),"rb")
print("location of decompressed file:")
out = input()

h=f.read(16)
w=f.read(16)
print(h,w)

img = np.zeros((h,w),dtype=np.uint8)

img[:,:] = 255

y=0
startX=-1
while y<h:
	try:
		y = f.read(16)
		numBlack = f.read(8)
	except:
		break
	
	#print(n)
	
	for i in range (0,numBlack):
		twobit = f.read(1)
		if twobit:
			x=f.read(15)
		else:
			x=f.read(7)
			
		twobit = f.read(1)
		if twobit:
			dx=f.read(15)
		else:
			dx=f.read(7)
		#print(x,dx)
		img[y,x:x+dx] = 0

#for y in range(0,h):
#	for x in range(0,w):
#		item = f.read(1)
#		#print(item)
#		img[y][x] = np.uint8(item*255)

f.close()

cv2.imwrite(out,img)

#oriimg = np.uint8(cv2.imread("xkcd.bmp",0))
#diff= np.abs(img-oriimg)
#cv2.imshow("diff",diff)
cv2.waitKey(0)
