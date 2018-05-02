# test Temperature and humidity sensor (Si7006-A20)
# https://www.silabs.com/documents/public/data-sheets/Si7006-A20.pdf
#
from pysense import Pysense
from SI7006A20 import SI7006A20
#from network import WLAN
import pycom
import micropython
import machine
import time
import os
import utime
#import socket
#import config

# wlan = WLAN(mode=WLAN.STA)
# mychannel = 0;

def c_to_f(c):
    return (c/5) * 9 + 32

# def connect_with_wifi():
#     nets = wlan.scan()
#     for net in nets:
#         if net.ssid == config.ssid:
#             print("Net SSID :{}".format(net.ssid))
#             print("RSSI: {}".format(net.rssi))
#             wlan.connect(net.ssid, auth=(WLAN.WPA2_ENT, config.username, config.password), identity=config.username, timeout=5000)
#             while not wlan.isconnected():
#                 machine.idle()
#             print("Connected with ictp-secure", end=" ")
#             global mychannel;
#             mychannel = net.channel
#             print("SSID {} RSSI {} Channel {}".format(net.ssid, net.rssi, net.channel))
#             break;
#
# def set_time():
#     rtc = machine.RTC()
#     rtc.init((2015, 1, 1, 1, 0, 0, 0, 0))
#     print("Before network time adjust", rtc.now())
#     print('Setting RTC using Sodaq time server')
#     time.sleep(2)
#     s=socket.socket()
#     addr = socket.getaddrinfo('time.sodaq.net', 80)[0][-1]
#     s.connect(addr)
#     s.send(b'GET / HTTP/1.1\r\nHost: time.sodaq.net\r\n\r\n')
#     ris=s.recv(1024).decode()
#     s.close()
#     print("----------------- Web page read:")
#     print(ris)
#     print("--------------------------------")
#     rows = ris.split('\r\n')            # transform string in list of strings
#     # seconds = rows[9]
#     seconds = 1525205163 #rows[7]
#     print("After network time adjust")
#     rtc.init(utime.localtime(int(seconds)))
#     print(rtc.now())

class TempHumidity():
    py = None #Pysense()
    tempHum = None #SI7006A20(py)
    tf = None
    file_path = None
    tmp_file  = None
    rtc = None
    def __init__(self):
        self.py = Pysense()
        self.tempHum = SI7006A20(self.py)
        self.rtc = machine.RTC();
        try:
            os.listdir('/flash/log')
        except OSError:
            os.mkdir('/flash/log')
        self.file_path = '/flash/log'
        self.tmp_log = 'tmp.log'
        self.tf = open('/flash/log/tmp.log', 'w+')

    def measure(self ):
      with open('/flash/log/tmp1.log', 'w+') as f:
        for i in range(5):
            tmp = self.tempHum.temp()
            hum = self.tempHum.humidity()
            t = rtc.now()
            print(t, tmp, hum)
            # print("Temperature: {} in Degrees".format(temperature)))
            # f.write("Temperature : " + str(temperature) + "\n")
            # if( count % 3 == 0):
            #     h
            #     print("Humidity: {}".format(humidity))
            #     f.write("Humidity: " + str(humidity) + "\n");
            #     #count = 0
            time.sleep(10)


    def __del__(self):
        if( not self.tf.closed()):
            self.tf.close();
# except Exception as e:
#     print(e)
#     print(dir(e))
# finally:
#     tf.close()
#     hf.close()
#connect_with_wifi()
#set_time()
# rtc = machine.RTC()
# seconds = 1525205163 #rows[7]
# print("After network time adjust")
# rtc.init(utime.localtime(int(seconds)))
# print(rtc.now())
p1 = TempHumidity()
p1.measure()
