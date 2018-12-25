import numpy as np
import cv2
import struct
from BitWriter import BitFile

print("image to compress:")
img = np.uint8(cv2.imread(input(),0)/255)

h,w=img.shape[:2]
print("output location:")
f=BitFile(input(),"wb")

f.write(h,16)
f.write(w,16)


for y in range(0,h):
	row = img[y]
	
	startX=0
	currentBlack=False
	
	numBlack=0
	for x in range(0,w):
		item = row[x]
		
		if item==0 and not currentBlack:
			numBlack+=1
			currentBlack=True
		if item==1 and currentBlack:
			currentBlack=False
		
	startX=0
	currentBlack=False
	
	
	if numBlack>0:
		f.write(y,16)
		f.write(numBlack,8)
		#print(y)
		#print(numBlack)
	
		lastn=-1
		for x in range(0,w):
			item = row[x]
			#print(item)
			
			n=-1
			if item==0 and not currentBlack:
				startX=x
				n=startX*1
				currentBlack=True
			if item==1 and currentBlack:
				n = x-startX
				currentBlack=False
				
			if not n==-1:
				lastn=n*1
				#print(x,n)
				if n>127:
					f.write(1,1)
					f.write(n,15)
				else:
					f.write(0,1)
					f.write(n,7)
		if currentBlack:
			#print(w-lastn)
			n=w-lastn
			
			if not n==-1:
				lastn=n*1
				#print(x,n)
				if n>255:
					f.write(1,1)
					f.write(n,15)
				else:
					f.write(0,1)
					f.write(n,7)
	
f.close()

