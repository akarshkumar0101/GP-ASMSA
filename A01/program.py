import numpy as math
import cv2

#rgb, bgr

def greyscale(img):
    newimg = 0.2*img[:,:,2]+0.7*img[:,:,1]+0.1*img[:,:,0]
    newimg = math.uint8(newimg)
    return newimg

def blackWhite(img, threshold=128):
    newimg=img*1
    newimg[newimg<=128] = 0
    newimg[newimg>128] = 255
    return newimg

def desaturate(img,percent=.5):
    newimg = img*1
    greyimg = greyscale(img)
    newimg[:,:,0] = newimg[:,:,0]*(1-percent)+greyimg[:,:]*percent
    newimg[:,:,1] = newimg[:,:,1]*(1-percent)+greyimg[:,:]*percent
    newimg[:,:,2] = newimg[:,:,2]*(1-percent)+greyimg[:,:]*percent
    newimg = math.uint8(newimg)
    return newimg

def contrast(img,factor=1):
    newimg = img*1
    newimg = math.float16(newimg)
    newimg[:,:,:] = (newimg[:,:,:]-128)*factor+128
    newimg[newimg>255] = 255
    newimg[newimg<0] = 0
    newimg = math.uint8(newimg)
    return newimg

img1ori = cv2.imread("input/image1.png",cv2.IMREAD_COLOR)
img2ori = cv2.imread("input/image2.png",cv2.IMREAD_COLOR)
img3ori = cv2.imread("input/image3.png",cv2.IMREAD_COLOR)

################### PART 1A ##################

img1 = greyscale(img1ori)
cv2.imwrite("output/pic_1_a.png",img1)

################### PART 1B ##################
img1 = blackWhite(img1)
cv2.imwrite("output/pic_1_b.png",img1)

################### PART 1C ##################

for i in range(0,11):
    img1 = img1ori*1
    img1 = desaturate(img1,i/10)
    cv2.imwrite("output/pic_1_c_"+str(i)+".png",img1)    

################### PART 1D ##################

for i in range(5,16):
    img1 = img1ori*1
    img1 = contrast(img1,i/10)
    cv2.imwrite("output/pic_1_d_"+str(i-5)+".png",img1)    


################### PART 2A ##################

img2 = img2ori*1
y,x = img2.shape[:2]

matrix = math.array([[-1,0,x],[0,1,0],[0,0,1]],math.float32)

img2 = cv2.warpPerspective(img2,matrix,(x,y))

cv2.imwrite("output/pic_2_a.png",img2)   

################### PART 2B ##################

theta = -30/180*math.pi
costheta = math.cos(theta)
sintheta = math.sin(theta)

img2 = img2ori*1
y,x = img2.shape[:2]

matrix1 = math.array([[1,0,-x],[0,1,-y],[0,0,1]],math.float32)
matrix2 = math.array([[costheta,sintheta,0],[-sintheta,costheta,0],[0,0,1]],math.float32)
matrix3 = math.array([[1,0,x],[0,1,y],[0,0,1]],math.float32)

M = matrix3.dot(matrix2).dot(matrix1)

img2 = cv2.warpPerspective(img2,M,(x,y))

cv2.imwrite("output/pic_2_b.png",img2)


################### PART 2C ##################

img1 = img1ori*1
img2 = img2ori*1
img3 = img3ori*1

y,x = img1.shape[:2]
ptsimg1 = math.float32([[0,0],[x,0],[x,y],[0,y]])

y,x = img2.shape[:2]
ptsimg2 = math.float32([[0,0],[x,0],[x,y],[0,y]])

pts1 = math.float32([[150,87],[330,160],[338,402],[182,293]])
pts2 = math.float32([[330,160],[510,78],[482,287],[338,402]])

squarepts = math.float32([[0,0],[300,0],[300,300],[0,300]])


y,x = img3.shape[:2]

Mtrans1 = cv2.getPerspectiveTransform(ptsimg1,pts1)
Mtrans2 = cv2.getPerspectiveTransform(ptsimg2,pts2)

img1trans = cv2.warpPerspective(img1,Mtrans1,(x,y))
img2trans = cv2.warpPerspective(img2,Mtrans2,(x,y))

img3 = img3ori*1
newimg = img3
trans = img1trans+img2trans

mask = trans[:,:,:] !=0
newimg[mask] = trans[mask]

cv2.imwrite("output/transformed_perspective.png",trans)
cv2.imwrite("output/pic_2_c.png",newimg)

cv2.waitKey(0)
cv2.destroyAllWindows()