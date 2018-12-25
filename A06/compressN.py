import cv2
import numpy as np
import struct
from BitWriter import BitFile

class CompressedImageWriter:
    def __init__(self,name,w,h):
        self.f=open(name,"wb")
        self.f.write(b'XKCD')
        self.f.write(struct.pack("<HH",w,h))
    def write(self,n,c):
        c=int(c)
        while n>0:
            if n<128:
                b=n*2+c
                b=struct.pack("<B",b)
                self.f.write(b)
                n-=n
            else:
                b=127*2+c
                b=struct.pack("<B",b)
                self.f.write(b)
                n-=127
    def close(self):
        self.f.close()
# <H
# <B

n=7
img=cv2.imread("xkcd.bmp",0)/255
h,w=img.shape[:2]
#out=CompressedImageWriter("test.xkcd",w,h)
out=BitFile("test.xkcd%d"%n,"wb")
out.writeBytesNow(b'XKCD')
out.write(w,16)
out.write(h,16)

for row in img:
    color=row[0]
    count=0
    for item in row:
        if item==color:
            count+=1
        else:
            #print(color,count)
            while count>=2**n:
                out.write(2**n-1,n)
                count-=2**n-1
                out.write(color,1)
            out.write(count,n)
            out.write(color,1)
            color=item
            count=1
out.close()
