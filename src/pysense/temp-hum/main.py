# test Temperature and humidity sensor (Si7006-A20)
# https://www.silabs.com/documents/public/data-sheets/Si7006-A20.pdf
#
from pysense import Pysense
from SI7006A20 import SI7006A20
import pycom
import micropython
import machine
import time
import os


def c_to_f(c):
    return (c/5) * 9 + 32

def set_time():
    rtc = machine.RTC()
    rtc.init((2015, 1, 1, 1, 0, 0, 0, 0))
    print("Before network time adjust", rtc.now())
    print('Setting RTC using Sodaq time server')
    time.sleep(2)
    s=socket.socket()
    addr = socket.getaddrinfo('time.sodaq.net', 80)[0][-1]
    s.connect(addr)
    s.send(b'GET / HTTP/1.1\r\nHost: time.sodaq.net\r\n\r\n')
    ris=s.recv(1024).decode()
    s.close()
    print("----------------- Web page read:")
    print(ris)
    print("--------------------------------")
    rows = ris.split('\r\n')            # transform string in list of strings
    # seconds = rows[9]
    seconds = rows[7]
    print("After network time adjust")
    rtc.init(utime.localtime(int(seconds)))
    print(rtc.now())
    
class TempHumidity():
    py = None #Pysense()
    tempHum = None #SI7006A20(py)
    tf = None
    file_path = None
    tmp_file  = None

    def __init__(self):
        self.py = Pysense()
        self.tempHum = SI7006A20(self.py)
        try:
            os.listdir('/flash/log')
        except OSError:
            os.mkdir('/flash/log')
        self.file_path = '/flash/log'
        self.tmp_log = 'tmp.log'
        self.tf = open('/flash/log/tmp.log', 'w+')

    def measure(self ):
      with open('/flash/log/tmp1.log', 'w+') as f:
        count = 1
        while count <= 15:
            temperature = self.tempHum.temp()
            print("Temperature: {} in Degrees, {} in Farenheight".format(temperature, c_to_f(temperature)))
            f.write("Temperature : " + str(temperature) + "\n")
            if( count % 3 == 0):
                humidity = self.tempHum.humidity()
                print("Humidity: {}".format(humidity))
                f.write("Humidity: " + str(humidity) + "\n");
                #count = 0
            time.sleep(10)
            count = count + 1;

    def __del__(self):
        if( not self.tf.closed()):
            self.tf.close();

# except Exception as e:
#     print(e)
#     print(dir(e))
# finally:
#     tf.close()
#     hf.close()
p1 = TempHumidity()
p1.measure()
