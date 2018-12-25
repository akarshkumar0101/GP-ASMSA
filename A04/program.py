import cv2
import numpy as np


def blurImage(img):
    gausskernver = cv2.getGaussianKernel(7,sigma=2)
    
    gausskernhor = gausskernver.transpose()
    gausskern = np.multiply(gausskernver,gausskernhor)
    return cv2.filter2D(img,-1,gausskern)

def energyToImg(I):
    img = np.uint8(I) 
    return img
def mapToImg(O):
    img = O/np.max(O)
    img*=255.9
    img=np.uint8(img)
    return img

def generateEnergy(img):
    edge_kernel=np.float32([[1,2,1],[0,0,0],[-1,-2,-1]])
    Iy=cv2.filter2D(img*1.0,-1,edge_kernel)
    Ix=cv2.filter2D(img*1.0,-1,edge_kernel.T)
    I=(Ix*Ix+Iy*Iy)**.5
    #I = np.abs(Ix)+np.abs(Iy)
    
    #step = .9*np.average(I)+.1*np.max(I)
    #I[I<step] = 0
    #I[I>=step] = 1
    
    I-=np.min(I)
    I/=np.max(I)
    I*=255.9
    return I

def generateVerMap(img, I):
    O = I*0
    
    for i in range(1,len(I)):
        row=O[i-1]*1
        left=np.roll(row,1)
        left[0]=10000
        left[-1]=10000
        right=np.roll(row,-1)
        right[0]=10000
        right[-1]=10000
        row[0]=10000
        row[-1]=10000
        x=np.vstack((left,row,right))
        x=x.min(axis=0)
        x+=I[i]
        O[i]=x        
    return O

def generateHorMap(img, I):
    O = I*0
    
    for i in range(1,len(I[0])):
        col = O[:,i-1]*1
        
        down=np.roll(col,1)
        down[0]=10000
        down[-1]=10000
        
        up=np.roll(col,-1)
        up[0]=10000
        up[-1]=10000
        col[0]=10000
        col[-1]=10000
        
        x=np.vstack((down,col,up))
        x=x.min(axis=0)
        x+=I[:,i]
        O[:,i]=x  
    
    return O

def getVerSeam(O):
    h,w = O.shape[:2]	
    	
    x = np.argmin(O[h-1])
    path=[[x,h-1]]
    while path[0][1]>0:
    	x,y=path[0]
    	y-=1
    	mid=O[y,x]
    	left=mid
    	if x>0:
    		left=O[y,x-1]
    	right=mid
    	if x<w-1:
    		right=O[y,x+1]
    	
        
    	if left<mid and left<right:
    		path.insert(0,[x-1,y])
    	elif right<mid and right<left:
    		path.insert(0,[x+1,y])
    	else:
            path.insert(0,[x,y])
    return np.array(path)

def getHorSeam(O):
    h,w = O.shape[:2]
    	
    y = np.argmin(O[:,w-1])
    path=[[w-1,y]]
    while path[0][0]>0:
    	x,y=path[0]
    	x-=1
    	mid=O[y,x]
    	down=mid
    	if y<h-1:
    		down=O[y+1,x]
    	up=mid
    	if y>0:
    		up=O[y-1,x]
    	
    	if down<mid and down<up:
    		path.insert(0,[x,y+1])
    	elif up<mid and up<down:
    		path.insert(0,[x,y-1])
    	else:
            path.insert(0,[x,y])
    return np.array(path)

def getSeams(O, numSeams):
    seams = []
    h,w = O.shape[:2]
    
    for i in range (numSeams):
        x = np.argmin(O[h-1])
        path=[[x,h-1]]
        O[h-1][x] = 10000
        while path[0][1]>0:
            x,y=path[0]
            y-=1
            mid=O[y,x]
            left=mid
            if x>0:
                left=O[y,x-1]
            right=mid
            if x<w-1:
                right=O[y,x+1]
            nextx = x
            if left<mid and left<right:
                nextx = x-1
            elif right<mid and right<left:
                nextx = x+1
            
            path.insert(0,[nextx,y])
            O[y][nextx] = 10000
        seams.append(path)
        
    return np.array(seams)

def removeVerSeam(img,seam):
    i=0
    rows=[]
    
    for row in img:
        x,y=seam[i]
        newrow = np.vstack((row[:x],row[x+1:]))
        rows.append(newrow)
        i+=1
    img=np.stack(rows)
    return img

def removeHorSeam(img,seam):
    i=0
    cols=[]
    for i in range (0,len(img[0])):
        col = img[:,i]
        x,y=seam[i]
        newcol = np.vstack((col[:y],col[y+1:]))
        
        cols.append(newcol)
        
    cols = np.array(cols)
    
    rows = [cols[:,0]]
    for i in range (1,len(img)-1):
        rows.append(cols[:,i])
    img = np.array(rows)
    return img

def removeSeams(img, seams):
    
    #print(seams[:,0])
    seams = np.array(sorted(seams, key=lambda x: x[0][0], reverse=True))
    #print(seams[:,0])
    
    for seam in seams:
        img = removeVerSeam(img,seam)
    
    return img

def addColorSeam(img,seam):
    i=0
    rows=[]
    for row in img:
        x,y=seam[i]
        rawpixel = (np.float32(row[x])+np.float32(row[x+1]))/2
        pixel = np.uint8(rawpixel)
        newrow = np.vstack((row[:x],pixel,row[x:]))
        rows.append(newrow)
        i+=1
    img=np.stack(rows)
    
    return img

def retarget(img, imgbw, finalw,finalh):
    h,w = img.shape[:2]
    
    while w>finalw:
        img = removeFirstVerSeam(img)
        print(str(w)+" "+str(finalw))
        h,w = img.shape[:2]
    while h>finalh:
        img = removeFirstHorSeam(img)
        print(str(h)+" "+str(finalh))
        h,w = img.shape[:2]
        
    return img

def drawSeam(img, seam):
    for x,y in seam:
        img[y][x] = 255
    return img

def removeFirstVerSeam(img):
    imgbw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    I = generateEnergy(imgbw)
    O = generateVerMap(imgbw,I)
    seam = getVerSeam(O)
    img = removeVerSeam(img, seam)
    return img
def removeFirstHorSeam(img):
    imgbw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    I = generateEnergy(imgbw)
    O = generateHorMap(imgbw,I)
    seam = getHorSeam(O)
    img = removeHorSeam(img, seam)
    return img

imgori=cv2.imread("input/image1.png")

imgoribw = cv2.cvtColor(imgori, cv2.COLOR_RGB2GRAY)
img = imgori*1
imgbw = imgoribw*1

cv2.imwrite("output/ori.png",img)


### 4a
#rock = cv2.imread("input/removerock.jpg",cv2.IMREAD_GRAYSCALE)
#rock = rock[::3,::3]
#rock = -rock
#I = generateEnergy(imgori)
#I+=rock
#O = generateVerMap(I)
#cv2.imwrite("output/rockmap.png",mapToImg(O))


### 1a
Iori = generateEnergy(imgbw)
cv2.imwrite("output/pic_1_a.png",energyToImg(Iori))
### 1b
Ovori = generateVerMap(imgbw,Iori)
Ohori = generateHorMap(imgbw,Iori)
cv2.imwrite("output/pic_1_b.png",mapToImg(Ovori))
cv2.imwrite("output/pic_1_b_hor.png",mapToImg(Ohori))

Ohori = generateHorMap(imgbw,Iori)
#cv2.imwrite("output/pic_1_c.png",mapToImg(Oh))

### 1c
vseam = getVerSeam(Ovori)
hseam = getHorSeam(Ohori)

img = drawSeam(img,vseam)

I=drawSeam(Iori,vseam)

Ovdrawn = drawSeam(mapToImg(Ovori),vseam)

cv2.imwrite("output/pic_1_c_0.png",img)
cv2.imwrite("output/pic_1_c_1.png",I)
cv2.imwrite("output/pic_1_c_2.png",Ovdrawn)

### 1d
img = removeVerSeam(img,vseam)
cv2.imwrite("output/pic_1_d.png",img)

### 1e
for i in range(50):
    img = removeFirstVerSeam(img)
cv2.imwrite("output/pic_1_e.png",img)

### 2a
Iori = generateEnergy(imgbw)
img = imgori*1
I = Iori*1
img = drawSeam(img,hseam)
I = drawSeam(I,hseam)
Ohdrawn = drawSeam(mapToImg(Ohori),hseam)

cv2.imwrite("output/pic_2_a_0.png",img)
cv2.imwrite("output/pic_2_a_1.png",I)
cv2.imwrite("output/pic_2_a_2.png",Ohdrawn)


### 2b
img = imgori*1
for i in range(50):
    img = removeFirstHorSeam(img)
cv2.imwrite("output/pic_2_b.png",img)


### 3b
print("3b")
##320x240, 320x320, 640x480, and 640x640
img = imgori*1
imgbw = imgoribw*1
img = retarget(img,imgbw,320,240)
cv2.imwrite("output/pic_3_b_0.png",img)
img = imgori*1
imgbw = imgoribw*1
img = retarget(img,imgbw,320,320)
cv2.imwrite("output/pic_3_b_1.png",img)
img = imgori*1
imgbw = imgoribw*1
img = retarget(img,imgbw,640,480)
cv2.imwrite("output/pic_3_b_2.png",img)
img = imgori*1
imgbw = imgoribw*1
img = retarget(img,imgbw,640,640)
cv2.imwrite("output/pic_3_b_3.png",img)

