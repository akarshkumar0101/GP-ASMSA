import numpy as np
import cv2
import struct
from BitWriter import BitFile

f=BitFile("test.output","wb")
f.write(1,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)

f.write(1,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)

f.write(1,1)
f.write(1,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)
f.write(0,1)

f.close()
