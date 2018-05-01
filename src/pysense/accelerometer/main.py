# test accelerometer (LIS2HH12)
# www.st.com/resource/en/datasheet/lis2hh12.pdfanslations/en.DM00096789.pdf
# based on this example
# # https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/pysense-examples.html#pysense-examples
#
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from math import sqrt
import pycom
import micropython
import machine
import time


pycom.heartbeat(False);
py = Pysense()
acc = LIS2HH12(py)


# def symbolizedacc():
#     r1 = acc.read();
#     t1 = sqrt(r1[0]**2 +  r1[1]**2 + r1[2]**2)
#     time.sleep(4)
#     r2 = acc.read();
#     t2 = sqrt(r2[0]**2 +  r2[1]**2 + r2[2]**2)
#     s = (t2  - t1)
#     print("Speeding {}".format(s))
#     print('X, Y, Z:',r1)
#     print('Roll:', acc.roll())
#     print('Pitch:', acc.pitch())
#     print('Yaw:', acc.yaw())
#     if(s < 50 ):
#         print("green")
#         pycom.rgbled(0x007f00) # green
#     elif(s in  range(51,1400)):
#         print("yellow")
#         pycom.rgbled(0x3346ff) # yellow FFFF00
#     elif( s >= 1400):
#         pycom.rgbled(0x7f0000) # red
#         print("red")

def pendulum():
    print('X, Y, Z:',acc.read())
    print('Roll:', acc.roll())
    print('Pitch:', acc.pitch())
    print('Yaw:', acc.yaw())
    time.sleep(2)


count = 1
with open('/flash/log/pendulum.txt', 'w') as f:
    while count < 100:
        r = acc.read()
        print(str(r))
        f.write(str(r)+"\n")
        time.sleep(1)
        count += 1
