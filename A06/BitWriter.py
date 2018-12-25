import struct,random

class Rectangle:
    def __init__(self,w,h):
        self.w=w
        self.h=h
    def area(self):
        return self.w*self.h
    def __str__(self):
        return "rectangle: width=%f height=%f"%(self.w,self.h)
    def __add__(self,rect):
        return Rectangle(self.w+rect.w,self.h+rect.h)
    

class BitFile:
    def __init__(self,filename,rights):
        self.f=open(filename,rights)
        self.buffer=0
        self.bitInBuffer=0
    def write(self,num,numOfBits):
        num=int(num)
        for i in range(numOfBits):
            bit=num%2
            num//=2
            self.buffer*=2
            self.buffer+=bit
            self.bitInBuffer+=1
            self._houseKeeping()
    def writeBytesNow(self,data):
        self.f.write(data)
    def read(self,numOfBits):
        while(self.bitInBuffer-numOfBits<0):
            self.bitInBuffer+=8
            self.buffer*=256
            data=self.f.read(1)
            #print repr(data)
            self.buffer+=struct.unpack("B",data)[0]
        num=0
        for i in range(numOfBits):
            q=2**(self.bitInBuffer-1)
            #print q,self.buffer
            bit=1 if q<=self.buffer else 0
            if bit==1:
                self.buffer-=q
            self.bitInBuffer-=1
            num+=bit*(2**i)
        return num
    def _houseKeeping(self):
        if self.bitInBuffer==8:
            self.f.write(struct.pack("B",self.buffer))
            self.buffer=0
            self.bitInBuffer=0
    def close(self):
        try:
            if self.bitInBuffer:
                self.f.write(struct.pack("B",self.buffer*(2**(8-self.bitInBuffer))))
        except:
            pass
        self.f.close()
    


if __name__ == "__main__":
    num=[]
    bits=[]
    for i in range(15):
        bits.append(random.randint(2,18))
        num.append(random.randint(0,2**(bits[-1]-1)))
        

    #0001 0000
    f=BitFile("test.output","wb")
    for n,b in zip(num,bits):
        f.write(n,b)
    f.close()
    f=BitFile("test.output","r")
    for b in bits:
        print(f.read(b))
    f.close()
    print(num)



    rect1=Rectangle(5,6)
    rect2=Rectangle(1,2)
    print(rect1)
    print(rect2)
    print(rect1+rect2)
