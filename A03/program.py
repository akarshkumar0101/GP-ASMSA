import cv2
import numpy as np

## SOME CODE BY SEWARD:
def panorama(img1, img2):
    img1gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    img2gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    sift = cv2.ORB_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1gray,None)
    kp2, des2 = sift.detectAndCompute(img2gray,None)
    
    bf = cv2.BFMatcher()
    
    # Match descriptors.
    matches = bf.knnMatch(des1,des2,k=2)
    
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    
    #cv2.imshow("mask",mask)
    
    #img3=cv2.warpPerspective(img1,M,(0,0))
    
    h,w=img1.shape[:2]
    corners=[[[0,0],[w,0],[w,h],[0,h]]]
    minx=miny=0
    maxx=w
    maxy=h
    perspectCorners=cv2.perspectiveTransform(np.float32(corners),M)
    minx=min(minx,np.min(perspectCorners[:,:,0]))
    maxx=max(maxx,np.max(perspectCorners[:,:,0]))
    miny=min(miny,np.min(perspectCorners[:,:,1]))
    maxy=max(maxy,np.max(perspectCorners[:,:,1]))
    
    T=np.float32([[1,0,-minx],[0,1,-miny],[0,0,1]])
    
    img1_t=cv2.warpPerspective(img1,T.dot(M),(int(maxx-minx),int(maxy-miny)))
    cv2.imwrite("output/t2_a.jpg",img1_t)
    img2_t=cv2.warpPerspective(img2,T,(int(maxx-minx),int(maxy-miny)))
    cv2.imwrite("output/t2_b.jpg",img2_t)
    
    map=img1_t==(0,0,0)
    map=cv2.dilate(np.uint8(map),np.ones((15,15),np.uint8))*255
    map=cv2.blur(map,(15,15))*1.0
    img3=np.uint8((img1_t*(255.0-map)+img2_t*map)/255)
    
    return img3

def circleCorners(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(img, 100, 0.01, 25,blockSize=10)
    for corner in corners:
        x,y=corner[0]
        cv2.circle(img, (x,y), 15, 0, -1)
    return img


img1ori = cv2.imread("input/ak_image1.jpg")
img2ori = cv2.imread("input/ak_image2.jpg")
img3ori = cv2.imread("input/ak_image3.jpg")
img4ori = cv2.imread("input/ak_image4.jpg")
#img1ori=img1ori[::5,::5]
#img2ori=img2ori[::5,::5]
#img3ori=img3ori[::5,::5]
#img4ori=img4ori[::5,::5]
#img1grayori = cv2.cvtColor(img1ori, cv2.COLOR_RGB2GRAY)
#img2grayori = cv2.cvtColor(img2ori, cv2.COLOR_RGB2GRAY)

#img1gray=img1grayori*1
#img2gray=img2grayori*1
#img1=cv2.resize(img1,(0,0),fx=.25,fy=.25)
#img2=cv2.resize(img2,(0,0),fx=.25,fy=.25)



img1 = img1ori*1
img2 = img2ori*1
img3 = img3ori*1
img4 = img4ori*1

pan = panorama(img1,img2)
pan = panorama(pan,img3)


cv2.imwrite("output/panorama.jpg",pan)

#corners=cv2.cornerHarris(img1, 2,3,0.04)


cv2.waitKey(0)
cv2.destroyAllWindows()
