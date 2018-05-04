"""
---------------------------------------------------------------------
Test1 grove temperature/humidity sensor DHT11
https://www.seeedstudio.com/Grove-TempHumi-Sensor-p-745.html
#
Author: Marco Rainone - Wireless Lab ICTP
email: mrainone@ictp.it
Ver: 0.1
Last Update: 01/05/2018
Based on this work:
https://github.com/JurassicPork/DHT_PyCom/tree/pulses_get
code released with MIT License (MIT)
---------------------------------------------------------------------
"""
# from:
# https://github.com/JurassicPork/DHT_PyCom/tree/pulses_get
#
import pycom
import time
import machine
from dth import DTH

from machine import I2C
# for grove sunlight sensor
from drvsi1145 import SI1145
# for grove oled display
from ssd1308 import SSD1308_I2C
from ssd1308 import SSD1308
from writer import Writer
# Font
import myfont
import gc

max = const(700)
min = const(300)
#def initialize_sunrize_oled():


def logger(data):
    try:
        os.listdir('/flash/log')
        print('/flash/log file already exists.')
    except OSError:
        print('/flash/log file does not exist. Creating it ...')
        os.mkdir('/flash/log')
    file_path = "/flash/log/"
    file_name = "temp-hum.csv"
    with open(file_path+file_name, 'w') as f:
        for item in data:
            f.write("{},{}\n".format(item[0],item[1]))


def connect_with_wifi():
    nets = wlan.scan()
    for net in nets:
        if net.ssid == config.ssid:
            print("Net SSID :{}".format(net.ssid))
            print("RSSI: {}".format(net.rssi))
            wlan.connect(net.ssid, auth=(net.sec, config.password), timeout=5000)
            while not wlan.isconnected():
                machine.idle()
            print("Connected with Fablab", end=" ")
            global mychannel;
            mychannel = net.channel
            print("SSID {} RSSI {} Channel {}".format(net.ssid, net.rssi, net.channel))
            break;

# connect the grove temperature/humidity (DHT11) sensor to digital connector J7 or J8
#  J7 connector: to I/O Pin 'P12'
#  J8 connector: to I/O Pin 'P11'

# Instantiate the DHT class with these parameters:
# 1) the pin number
# 2) type of sensor: 0 for DTH11, 1 for DTH22
th = DTH('P11',0)

# loop to read temperature / humidity from DHT11
#
i2c = I2C(0, I2C.MASTER, baudrate=100000)
sensor = SI1145(objI2C=i2c)
# use grove oled display
grove_oled_display = SSD1308_I2C(objI2C=i2c)
display = Writer(grove_oled_display, myfont)
gc.collect()            # free ram
Writer.set_clip(True, True)
time.sleep(2)
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P15 (J5 connector)
dpin = adc.channel(pin='P15')
data = []
# for i in range(20):
#     # Call read() method, which will return DHTResult object with actual values and error code.
        # grove_oled_display.clearDisplay();
        # uv = sensor.read_uv()
        # vi = sensor.read_visible()
        # ir = sensor.read_ir()
        # pr = sensor.read_prox()
        # print('{},{},{},{}\n'.format(uv,vi,ir,pr))
        # str_uv = 'u:{}'.format(uv)
        # str11 ='v:{}'.format(vi)
        # str_ir = 'i:{}'.format(ir)
        # str22 ='p:{}'.format(pr)
        #
        # # display strings
        #
        # # write str1
        # display.set_textpos(0, 4)            # set position (row, col)
        # display.printstring(str_uv)
        # gc.collect()            # free ram
        # # write str2
        # display.set_textpos(25, 20)          # set position (row, col)
        # display.printstring(str_ir)
        #
        # display.show()
        # time.sleep(5)
#
#         grove_oled_display.clearDisplay();
#
#     else:
#         print("Error reading sensor !")
#     time.sleep(2)
# logger(data)
def measure_light():
            grove_oled_display.clearDisplay();
            uv = sensor.read_uv()
            vi = sensor.read_visible()
            ir = sensor.read_ir()
            pr = sensor.read_prox()
            print('{},{},{},{}\n'.format(uv,vi,ir,pr))
            str_uv = 'u:{}'.format(uv)
            str11 ='v:{}'.format(vi)
            str_ir = 'i:{}'.format(ir)
            str22 ='p:{}'.format(pr)

            # display strings

            # write str1
            display.set_textpos(0, 4)            # set position (row, col)
            display.printstring(str_uv)
            gc.collect()            # free ram
            # write str2
            display.set_textpos(25, 20)          # set position (row, col)
            display.printstring(str_ir)

            display.show()
            time.sleep(5)

def measure_moisture():
    analog_val = apin()
    digital_val = dpin()

    percentage = ((analog_val - max)/(max - min)) * 100 ;
    str1 = 'M:{:0.2f}%'.format(percentage)
    print('Moisture:A:{}, A:{:0.2f}%, D:{}\n'.format(analog_val, percentage, digital_val))
    grove_oled_display.clearDisplay();
    gc.collect()
    display.set_textpos(0, 4)            # set position (row, col)
    display.printstring(str1)
    display.show()
    time.sleep(5)

def measure_temp_hum():
    result = th.read()
    if result.is_valid():
        temp = result.temperature
        hum = result.humidity
        print("Temperature: {} C".format(temp))
        print("Humidity: {}%".format(hum))
        data.append((temp, hum))

        str1 = 'Temp: {}'.format(temp)
        str2 = 'Hum: {}'.format(hum)
        display.set_textpos(0, 4)            # set position (row, col)
        display.printstring(str1)
        gc.collect()            # free ram
        # write str2
        display.set_textpos(25, 20)          # set position (row, col)
        display.printstring(str2)
        display.show()
        time.sleep(5)


while True:
    grove_oled_display.clearDisplay()
    measure_temp_hum()
    grove_oled_display.clearDisplay()
    measure_moisture()
    grove_oled_display.clearDisplay()
    measure_light()
