import cv2
import numpy as np
import itertools
import math

base_size = 900
step_size = int(round(base_size / 9))
dataZone = []
for y in range(50,base_size,step_size):
    for x in range(50,base_size,step_size):
        dataZone.append((y,x))

del dataZone[10]
del dataZone[15]
del dataZone[62]
del dataZone[67]


cap = cv2.VideoCapture(0)

def findPairs(contours, frame):
    if(len(contours)>1000):
        return [],[]
    moments=[(c,cv2.moments(c)) for c in contours]
    pairs=[]
    for a,b in itertools.combinations(moments,2):
        contourA,momentsA=a
        contourB,momentsB=b
        if momentsA['m00']>0 and momentsB['m00']>0:
            ax = momentsA['m10']/momentsA['m00']
            ay = momentsA['m01']/momentsA['m00']
            bx = momentsB['m10']/momentsB['m00']
            by = momentsB['m01']/momentsB['m00']
            areaA=momentsA['m00']
            areaB=momentsB['m00']
            areas=[areaA,areaB]
            areas.sort()
            x,y=areas
            p = x/y*25

            if math.hypot(ax-bx,ay-by)<1 and 1<p<10 and y>400:
                pairs+=(p,ax,ay,contourA,contourB),
    pairs.sort()
    points=[[[x,y]] for _,x,y,_,_ in pairs]
    contours=[]
    for _,_,_,ca,cb in pairs:
        contours+=ca,cb,
    return points,contours

def decode(frame):
	bits = []
	for p in dataZone:
		color = frame[p[0],p[1]]
		if 90 < color < 150:
			break
		bits.append(int((color>128)))
	return bits

corners=np.float32([[[750,750]],[[750,150]],[[150,150]],[[150,750]]])



def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

while(True):
    ret, frame = cap.read()
    thresh=np.uint8(frame>128)*255
    _,contours,_ = cv2.findContours(thresh[:,:,1]*1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    points,contours=findPairs(contours, frame)
    
    if len(points)==4:
        M=cv2.getPerspectiveTransform(np.float32(points), corners)
        code=cv2.warpPerspective(frame[:,:,1], M, (900,900))
        code=np.uint8(code)
        bits = decode(code)
        print(frombits(bits))
        code=cv2.resize(code,(140,140),interpolation=cv2.INTER_NEAREST)
        frame[:140,:140]=code[:,:,None]
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    for p in points:
        x,y=p[0]
        cv2.circle(frame,(int(x), int(y)), 5, (0,0,255), -1)

    cv2.imshow("QR Decoder",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
