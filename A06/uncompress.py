import numpy as np
import cv2
import struct

f=open("test.xkcd","rb")
m=[]
print(f.read(4))
w,h=struct.unpack("<HH",f.read(4))
print(w,h)
data=f.read()
for b in data:
	b=int(b)
	rl=b//2
	color=b%2
	m+=[color]*rl
img=np.uint8(m).reshape(h,w)*255
cv2.imwrite("uncompress.png",img)
