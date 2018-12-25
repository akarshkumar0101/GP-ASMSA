import numpy as math
import cv2

img1ori = cv2.imread("input/image1.jpg",cv2.IMREAD_COLOR)
img2ori = cv2.imread("input/image2.jpg",cv2.IMREAD_COLOR)

#rgb, bgr

##################### SECTION 1 ##########################
##########   PART A
img1 = img1ori*1

red = img1[:,:,2]
green = img1[:,:,1]

img1[:,:,1] = red
img1[:,:,2] = green

cv2.imwrite("output/pic_1_a.png",img1)

##########    PART B
img2 = img2ori*1

img2[:,:,1] = 0
img2[:,:,2] = 0

cv2.imwrite("output/pic_1_b.png",img2)

##########    PART C
img1 = img1ori*1

green = img1[:,:,1]
green = 255-green
img1[:,:,1] = green

cv2.imwrite("output/pic_1_c.png",img1)

##########    PART D
img2 = img2ori*1

#img2+=100
#img2[img2>255] = 255

img2[img2>155] = 255
img2[img2<=155] +=100


cv2.imwrite("output/pic_1_d.png",img2)


####################### SECTION 2 ######################
#########    PART A
img1 = img1ori*1

h,w = img1.shape[:2]
x = int(w/2-50)
y = int(h/2-50)

img1[y:y+100,x:x+100,1] = 255

cv2.imwrite("output/pic_2_a.png",img1)

#########    PART B
img1 = img1ori*1
img2 = img2ori*1

h,w = img1.shape[:2]
x1 = int(w/2-50)
y1 = int(h/2-50)

h,w = img2.shape[:2]
x2 = int(w/2-50)
y2 = int(h/2-50)

img2[y2:y2+100,x2:x2+100] = img1[y1:y1+100,x1:x1+100]

cv2.imwrite("output/pic_2_b.png",img2)


####################### SECTION 3 ######################
#numpy.std(array)
print("pixels: "+ str(math.size(img1ori)/3))
print("min intensity: "+ str(math.min(img1ori)))
print("max intensity: "+ str(math.max(img1ori)))
print("standard dev. of intensity: "+ str(math.std(img1ori)))
print("mean intensity: "+ str(math.mean(img1ori)))


####################### SECTION 4 ######################


#1520x800
redcolor = (52,34,178)
bluecolor = (110,59,60)
whitecolor = (255,255,255)

def fillCircle(img,x,y,r,color):
    r2=r*r
    h,w=img.shape[:2]
    for row in range(x-r,x+r):
        for col in range(y-r,y+r):        
            d2=(col-x)**2+(row-y)**2
            if d2<r2:
                img[row,col]=color
    return img

def angleTo(x1,y1,x2,y2):
    angle = math.arctan2(y1-y2,x2-x1)
    if(angle<0):
        angle+=2*math.pi
    return angle
def findIntersect(m1,b1,m2,b2):
    x=(b2-b1)/(m1-m2)
    y=m1*x+b1
    return (x,y)

def drawNormalStar(img, xc,yc,r,color=(0,0,0)):
    pointAngle = math.radians(36)

    for x in range(xc-r,xc+r):
        for y in range(yc-r,yc+r):
            
            if((x-xc)**2+(y-yc)**2<= r**2):
                for i in range (0,5):
                    pointx = xc+r*math.cos(i*2*math.pi/5-math.pi/2)
                    pointy = yc+r*math.sin(i*2*math.pi/5-math.pi/2)
                    
                    pointCenterAngle = angleTo(pointx,pointy,xc,yc)
                    pointCenterAngleLeft = pointCenterAngle - pointAngle/2
                    pointCenterAngleRight = pointCenterAngle + pointAngle/2
                    
                    angleFromPoint = angleTo(pointx,pointy,x,y)
                    
                    distFromPoint = math.sqrt((x-pointx)**2+(y-pointy)**2)
                    if(angleFromPoint>pointCenterAngleLeft and angleFromPoint<pointCenterAngleRight):
                        if(distFromPoint < 1.1*r):
                            img[y][x] = color
    
    return img

def getWidth(img):
    return img.shape[1]

def getHeight(img):
    return img.shape[0]


flagwidth = int(1235)
flagheight = int(flagwidth*10/19)
img = math.zeros((flagheight,flagwidth,3),dtype=math.uint8)
h,w=img.shape[:2]
img[:h] = redcolor

redstripe = 1
for i in range (0,13):
    
    if(redstripe==0):
        y1 = int(i/13.0 * h)
        y2 = int((i+1)/13.0*h)
        
        img[y1:y2] = whitecolor
        
    if(redstripe == 1):
        redstripe = 0
    else: 
        redstripe = 1
        
blueheight = int(7/13*flagheight)
bluewidth = int(.76*flagheight)
img[0:blueheight,0:bluewidth] = bluecolor

#fillCircle(img,240,240,100, (255,255,255))

starradius = int(.0308 * flagheight)

dimensione = int(.054 * flagheight)
dimensionf = int(.054 * flagheight)
dimensiong = int(.063 * flagheight)
dimensionh = int(.063 * flagheight)
dimensiong = int(.064 * flagheight)
dimensionh = int(.064 * flagheight)

for i in range(0,11):
    for j in range(0,9):
        if(i%2==j%2):
            drawNormalStar(img,i*dimensionh+dimensiong,j*dimensionf+dimensione,starradius,whitecolor)
         
cv2.imwrite("output/pic_4_a.png",img)

imgori = cv2.imread("input/flag.png",cv2.IMREAD_COLOR)

diff = imgori-img

diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)

minn = math.min(diff)
maxx = math.max(diff)
scale = 255/(maxx-minn)

diff -= minn
diff = math.array(diff, dtype=math.float)
diff *= scale
diff = math.array(diff, dtype=math.uint8)

cv2.imwrite("output/pic_4_b.png",diff)

cv2.imshow("American Flag by Akarsh Kumar",img)


cv2.waitKey(0)
cv2.destroyAllWindows()



