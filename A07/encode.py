import numpy as np
import cv2
import struct
from BitWriter import BitFile


#rgby
#bgr

def getColor(b):
	if b==0:
		return (0,0,0)
	if b==1:
		return (255,255,255)

def target(img, x, y, w, h, col, kx, ky):
	if w<0 and h<0:
		return
	img[y:y+h,x:x+w]=col
	target(img,x+kx,y+ky,w-2*kx,h-2*ky,255-col,kx,ky)
def drawCorners(img,w,h,tw,th):
	img[0:th,0:tw]=0
	img[int(th/5):int(4*th/5),int(tw/5):int(4*tw/5)]=255
	
	img[h-th:h,0:tw]=0
	img[int(h-4*th/5):int(h-th/5),int(tw/5):int(4*tw/5)]=255
	img[int(h-3*th/5):int(h-2*th/5),int(tw/5):int(4*tw/5)]=0
	img[int(h-3*th/5):int(h-2*th/5),int(2*tw/5):int(3*tw/5)]=255
	
	
	img[0:th,w-tw:w]=0
	img[int(2*th/5):int(3*th/5),int(w-4*tw/5):int(w-tw/5)]=255
	img[int(3*th/5):int(4*th/5),int(w-4*tw/5):int(w-3*tw/5)]=255
	img[int(1*th/5):int(2*th/5),int(w-2*tw/5):int(w-1*tw/5)]=255
	
	
	img[h-th:h,w-tw:w]=0
	img[int(h-3*th/5):int(h-2*th/5),int(w-4*tw/5):int(w-tw/5)]=255
	
	

def encode(img,bits):
	totalr=20
	data=0
	datai=0
	
	#datalen = np.unpackbits(len(bits))
	dataleni=0
	datalen = np.binary_repr(len(bits),10)
	print(len(bits))
	print(datalen)
	
	for c in range (totalr-1,-1,-1):
		totala = 4*c+5
		angle = 2*np.pi/totala
		for i in range (0,totala):
			maskr1 = r>=rmax/totalr*c
			maskr2 = r<=rmax/totalr*(c+1)
			maska1 = theta>=angle*i
			maska2 = theta<=angle*(i+1)
			mask = maskr1 & maskr2 & maska1 & maska2
			
			if dataleni<10:
				if datalen[dataleni]=='1':
					bit=1
				else:
					bit=0
				img[mask] = getColor(bit)
				dataleni+=1
				print(bit)
			elif datai<len(bits):
				bit= bits[datai]
				img[mask] = getColor(bit)
				datai+=1
			else:
				img[mask] = getColor(0)
			
			#if c==totalr-1 and i==2:
			# 	img[mask]=128
			
			data+=1
			mask = (r>rmax/totalr*c) & (r<rmax/totalr*(c+1))
			mask = (mask)&(theta>angle*i)&(theta<(angle*i+4*np.pi/180/(c+1)))
			#img[mask]=0
		mask = (r>rmax/totalr*c)&(r<rmax/totalr*c+2)
		img[mask]=0
	print(data)
	c=totalr
	mask = (r>rmax/totalr*c)&(r<rmax/totalr*c+2)
	img[mask]=0
	maskr1 = r>0
	maskr2 = r<np.max(r)
	maska1 = theta>0
	maska2 = theta<10*np.pi/180
	mask = maskr1 & maskr2 & maska1 & maska2
	#img[mask] = 0


a=64
print(a)
a=a>>1
print(a)

f=BitFile("in.txt","rb")
bits=[]
while 1:
	try:
		bits.append(f.read(1))
	except:
		break


#1720 bits, 215 bytes
#860 bits, 107 bytes

h=500
w=500
img = np.zeros((h,w,3),dtype=np.uint8)

img[:,:,:]=255

y,x=np.mgrid[0:h,0:w]

gridx = x-w/2
gridy = y-h/2

r=np.hypot(gridx,gridy)
rmax = h/2
theta=np.arctan2(gridy,gridx)
theta+=np.pi

w2 = int(w/2)
h2 = int(h/2)
#img[:w2,:h2] = getColor(0)
#img[w2:w,:h2] = getColor(1)
#img[:w2,h2:h] = getColor(2)
#img[w2:w,h2:h] = getColor(3)

encode(img,bits)

sqrsize = .05
#img[:int(sqrsize*w),:int(sqrsize*h)]=0
#img[w-int(sqrsize*w):,:int(sqrsize*h)]=0
#img[:int(sqrsize*w),h-int(sqrsize*h):]=0
#img[w-int(sqrsize*w):,h-int(sqrsize*h):]=0

tw = w/2-w/2/np.sqrt(2)-15
th = h/2-h/2/np.sqrt(2)-15
tw=int(tw)
th=int(th)
drawCorners(img,w,h,tw,th)
#target(img,0,0,int(2*tw/3),int(2*th/3),0,int(2*tw/3/10),int(2*th/3/10))
#target(img,w-int(2*tw/3),0,int(2*tw/3),int(2*th/3),0,int(2*tw/3/10),int(2*th/3/10))
#target(img,0,h-th,tw,th,0,int(tw/15),int(th/15))
#target(img,h-th,w-tw,tw,th,0,int(tw/15),int(th/15))

cv2.imshow("img",img)
cv2.imwrite("akarz.png",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

