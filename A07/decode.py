import numpy as np
import cv2
import struct
from BitWriter import BitFile
import itertools
import math
from reedsolo import RSCodec

def decode(img):
	
	y,x=np.mgrid[0:h,0:w]

	gridx = x-w/2
	gridy = y-h/2

	r=np.hypot(gridx,gridy)
	rmax = h/2
	theta=np.arctan2(gridy,gridx)
	theta+=np.pi

	
	filelenbits=[]
	filelen=-1
	bits=[]
	
	totalr=20
	data=0
	datai=0
	
	#datalen = np.unpackbits(len(bits))
	
	akarsh=0
	for c in range (totalr-1,-1,-1):
		totala = 4*c+5
		angle = 2*np.pi/totala
		for i in range (0,totala):
			readr=rmax/totalr*(c+.5)
			readtheta = -angle*(i+.5)-np.pi/2
			readx =int(readr*np.cos(readtheta)+w/2)
			ready= int(readr*np.sin(readtheta)+h/2)
			col = img[readx,ready]
			#print(i)
			if akarsh<10:
				#img[readx:readx+5,ready:ready+5] = 128
				akarsh+=1
			
			if col>128:
				bit=1
			else:
				bit=0
			#print(bit)
			if filelen==-1:
				filelenbits.append(bit)
				#print(bit)
				if len(filelenbits)==10:
					filelen=0
					fileleni=9
					for filelenbit in filelenbits:
						filelen+=filelenbit*(2**fileleni)
						fileleni-=1
					#print(filelen)
			elif datai<filelen:
				bits.append(bit)
				datai+=1
			
			data+=1
	#print(data)
	return bits



def getDataZone():
    img=np.zeros((28,28),dtype=np.uint8)

    #make the part where there will be data white
    img+=255
    img[:6,:6]=0
    img[-6:,:6]=0
    img[:6,-6:]=0
    img[-6:,-6:]=0
    #store all these locations in the x and y arrays
    #I will use this order to figure out how to put in data.
    #This is 640bits=80bytes
    x,y=np.where(img>0)
    return x,y

cap = cv2.VideoCapture(0)

def findPairs(contours):
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
            #percentage full (*25) the tracking dot is
            p=x/y*25
            if math.hypot(ax-bx,ay-by)<1 and 2<p<10 and y>400:
                #print(p)
                pairs+=(p,ax,ay,contourA,contourB),
    pairs.sort()
    points=[[[x,y]] for _,x,y,_,_ in pairs]
    contours=[]
    for _,_,_,ca,cb in pairs:
        contours+=ca,cb,
    return points,contours



h=500
w=500

tw = w/2-w/2/np.sqrt(2)-15
th = h/2-h/2/np.sqrt(2)-15
twm=tw/2
thm=th/2

corners=np.float32([[[h-thm,w-twm]],[[h-thm,twm]],[[thm,w-twm]],[[thm,twm]]])


while(True):
    ret, frame = cap.read()
    thresh=np.uint8(frame>60)*255
    _,contours,_ = cv2.findContours(thresh[:,:,1]*1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    points,contours=findPairs(contours)
    
    if len(points)==4:
        M=cv2.getPerspectiveTransform(np.float32(points), corners)
        code=cv2.warpPerspective(frame[:,:,1], M, (h,w))
        code[code<60] = 0
        code[code>=60]=255
        
        break
        #code=code*1.0
        #code-=np.min(code)
        #code/=np.max(code)
        #code*=255.99
        #code=code>200
        #code=code*255.0
        #code=np.uint8(code)
        codesmall=cv2.resize(code,(28,28))
        data=1-(codesmall>128)
        x,y=getDataZone()
        s=np.packbits(data[x,y])
        print(decode(s.tobytes()))
        

        
        code=cv2.resize(codesmall,(140,140),interpolation=cv2.INTER_NEAREST)
        #code=code>128
        #code=code*255.0
        #code=np.uint8(code)
        frame[:140,:140]=code[:,:,None]
        
        
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    for p in points:
        x,y=p[0]
        cv2.circle(frame,(int(x), int(y)), 5, (0,0,255), -1)

    cv2.imshow("img",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


img = cv2.imread("akarz.png")
img = code
bits = decode(code)


f=BitFile("out.txt","wb")
for bit in bits:
	print(bit)
	f.write(bit,1)
f.close()


cv2.imshow("code",code)
#cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

