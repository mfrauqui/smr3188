import pycom
import time

def dotmsg():
    pycom.rgbled(0x7f0000)
    print(".", end=" ")
    #pausemsg()
    time.sleep(1)

def pausemsg():
    pycom.rgbled(0x000000)
    print(" ", end=" ")
    time.sleep(5)

def linemsg():
    for i in range(3):
        dotmsg()
    time.sleep(5)

def morescode():
    for cycles in range(10):
     for dot in range(3):
        dotmsg()     #send a dot -- red
     pausemsg()   #send a pause -- yellow
     for dot in range(3):
        linemsg()    #send three dots - a line -- red
     pausemsg()   #send a pause -- yellow

pycom.heartbeat(False)
morescode()
