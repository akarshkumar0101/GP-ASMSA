import cv2
import numpy as np
import struct


class CompressedImageWriter:
	def __init__(self,name,w,h):
		self.f=open(name,"wb")
		self.f.write(b'XKCD')
		self.f.write(struct.pack(">HH",w,h))
	def write(self,n,c):
		c=int(c)
		while n>0:
			if n<128:
				b=n*2+c
				b=struct.pack(">B",b)
				self.f.write(b)
				n-=n
			else:
				b=127*2+c
				b=struct.pack(">B",b)
				self.f.write(b)
				n-=127
	def close(self):
		self.f.close()



img=cv2.imread("xkcd.bmp",0)/255
h,w=img.shape[:2]
out=CompressedImageWriter("test.xkcd",w,h)
for row in img:
	color=row[0]
	count=0
	for item in row:
		if item==color:
			count+=1
		else:
			out.write(count,color)
			color=item
			count=1
	out.write(count,color)
out.close()
