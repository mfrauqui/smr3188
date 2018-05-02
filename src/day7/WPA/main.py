from network import WLAN
import machine
import time
import ubinascii
import pycom
import config

wlan = WLAN(mode=WLAN.STA)
mychannel = 0;

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

def measure_rssi():
    data = []
    global mychannel
    for i in range(50):
        nets = wlan.scan()
        for net in nets:
            if net.ssid == config.ssid and net.channel == mychannel:
                print("SSID {} RSSI {} Channel {}".format(net.ssid, net.rssi, net.channel))
                symbolized(net.rssi)
                data.append(net.rssi)
                time.sleep(1)
    logger(data)


def symbolized(rssi):
    rssi = -rssi;
    if(rssi in range(25)):
        pycom.rgbled(0x7f0000)
    elif(rssi in range(25,60)):
        pycom.rgbled(0x7f7f00)
    else:
        pycom.rgbled(0x7f7fff)

def logger(data):
    try:
        os.listdir('/flash/log')
        print('/flash/log file already exists.')
    except OSError:
        print('/flash/log file does not exist. Creating it ...')
        os.mkdir('/flash/log')
    file_path = "/flash/log/"
    file_name = "rssi.log"
    with open(file_path+file_name, 'w') as f:
        f.write(str(data))

def set_time():
    rtc = machine.RTC()
    rtc.init((2015, 1, 1, 1, 0, 0, 0, 0))
    print("Before NTP adjust", time.localtime())
    print('Set RTC using ntp.org')
    rtc.ntp_sync("pool.ntp.org")
    time.sleep_ms(1000)
    print(rtc.now())
    print('Time set!')
    print("The time is now: ", time.localtime())
    print('----------------- end set rtc using ntp.org')


pycom.heartbeat(False)
connect_with_wifi()
print(wlan.ifconfig())
print(ubinascii.hexlify(machine.unique_id(),':').decode())
measure_rssi()
