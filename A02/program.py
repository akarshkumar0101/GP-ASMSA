import numpy as np
import cv2

#rgb, bgr
def grayscale(img):
    newimg = 0.2*img[:,:,2]+0.7*img[:,:,1]+0.1*img[:,:,0]
    newimg = np.uint8(newimg)
    return newimg

def blackWhite(img, threshold=128):
    newimg=img*1
    newimg[newimg<128] = 0
    newimg[newimg>=128] = 255
    return newimg
def averageDiff(img1,img2):
    newimg = img1-img2
    newimg = np.abs(newimg)
    avg = np.average(newimg)
    return avg
def normalizeDiff(img1,img2):
    img1=np.float32(img1)
    img2=np.float32(img2)
    newimg = img1-img2
    minn = np.min(newimg)
    maxx = np.max(newimg)
    scale = 255/(maxx-minn)
    newimg -=minn
    newimg*=scale
    newimg=np.uint8(newimg)
    return newimg

img1ori = cv2.imread("input/image1.png",cv2.IMREAD_COLOR)
img2ori = cv2.imread("input/image2.png",cv2.IMREAD_COLOR)
img1ori = img1ori[::4,::4,:]
img2ori = img2ori[::4,::4,:]


img1gray = grayscale(img1ori)
img2gray = grayscale(img2ori)

img1bw = blackWhite(img1gray)
img2bw = blackWhite(img2gray)

#### 1
boxkern = np.ones((5,5),np.float32)/25
horboxkern = np.ones((1,5),np.float32)/5
verboxkern = np.ones((5,1),np.float32)/5

hor = cv2.filter2D(img1ori,-1,horboxkern)
box = cv2.filter2D(img1ori,-1,boxkern)
ver = cv2.filter2D(hor,-1,verboxkern)



cv2.imwrite("output/pic_1_b.png",box)
cv2.imwrite("output/pic_1_d_0.png",hor)
cv2.imwrite("output/pic_1_d_1.png",ver)

print(averageDiff(grayscale(box),grayscale(ver)))

normalize = normalizeDiff(grayscale(box),grayscale(ver))
cv2.imwrite("output/pic_1_e.png",normalize)

##### 2
gausskernver = cv2.getGaussianKernel(3,sigma=1)
gausskernhor = gausskernver.transpose()
gausskern = np.multiply(gausskernver,gausskernhor)

circle = cv2.filter2D(img1ori,-1,gausskern)
hor = cv2.filter2D(img1ori,-1,gausskernhor)
ver = cv2.filter2D(hor,-1,gausskernver)

cv2.imwrite("output/pic_2_b.png",circle)
cv2.imwrite("output/pic_2_d_0.png",hor)
cv2.imwrite("output/pic_2_d_1.png",ver)

print(averageDiff(grayscale(circle),grayscale(ver)))

normalize = normalizeDiff(grayscale(circle),grayscale(ver))
cv2.imwrite("output/pic_2_e.png",normalize)

##### 3
edgekern = np.array([[1,0,-1],[0,0,0],[-1,0,1]])
diagedge = cv2.filter2D(img2gray,-1,edgekern)

edgekern1 = np.array([[1,0,-1]])
edgekern2 = edgekern1.transpose()


cv2.imwrite("output/pic_3_b.png",diagedge)

edge = cv2.filter2D(img2gray,-1,edgekern1)
cv2.imwrite("output/pic_3_d_0.png",edge)

edge = cv2.filter2D(edge,-1,edgekern2)
cv2.imwrite("output/pic_3_d_1.png",edge)

print(averageDiff(diagedge,edge))

normalize = normalizeDiff(diagedge,edge)
cv2.imwrite("output/pic_3_e.png",normalize)


###### 4
sharpkern = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
sharp = cv2.filter2D(img2ori,-1,sharpkern)

cv2.imwrite("output/pic_4_b.png",sharp)

###### 5

verkern = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
horkern = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
edge1 = cv2.filter2D(img1gray,-1,verkern)
edge2 = cv2.filter2D(img1gray,-1,horkern)

edge1bw = blackWhite(edge1)
edge2bw = blackWhite(edge2)

edge1f = np.float32(edge1bw)
edge2f = np.float32(edge2bw)

cornerf = (edge1f+edge2f)/2

corner = np.uint8(cornerf)
corner[corner<=128] = 0

cv2.imwrite("output/pic_5_horizontal_edge.png",edge1bw)
cv2.imwrite("output/pic_5_vertical_edge.png",edge2bw)
cv2.imwrite("output/pic_5_corner.png", corner)


cv2.waitKey(0)
cv2.destroyAllWindows()