import os
from pytrack import Pytrack
from L76GNSS import L76GNSS
import time
import LEDColors
import pycom
from network import WLAN

wlan = WLAN(mode=WLAN.STA)
#Enable GPS here
py = Pytrack()
gps = L76GNSS(py, timeout=30)


def open_log_file():
    try:
        os.listdir('/flash/log')
    except OSError:
        os.mkdir('/flash/log')

# stop the heartbeat
pycom.heartbeat(False)
led = LEDColors.pyLED()

led.setLED('red')

open_log_file()
logger = open('/flash/log/lat-long5.csv','w+');

(lat, lon, alt, hdop) = gps.position()
print("%s %s %s %s" %(lat, lon, alt, hdop))
logger.write('{},{},{},{},{}\n'.format('latitude', 'longitude', 'altitude', 'hdop', 'information'))
#while True:
for i in range(100):
    (lat, lon, alt, hdop) = gps.position()
    print("%s %s %s %s" %(lat, lon, alt, hdop))
    if (str(lat) == 'None'):
        led.setLED('red')
        print("I do not have a fix!")
    else:
        led.setLED('green')
        no_of_wifi = len(wlan.scan())
        logger.write('{},{},{},{},{}\n'.format(lat, lon, alt, hdop, no_of_wifi))
        print("%s, %s, %s, %s, %s" %(lat, lon, alt, hdop, no_of_wifi))
    time.sleep(10)
logger.close();
