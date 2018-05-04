from network import LoRa
import time
import binascii
import socket
import time
import pycom
import time
from machine import Pin
from dth import DTH
from machine import UART
import json


uart = UART(1, 115200)
th = DTH('P11',0)

lora = LoRa(mode=LoRa.LORAWAN, tx_power=14, region=LoRa.EU868)

app_eui = binascii.unhexlify('70B3D57ED000C391')
app_key = binascii.unhexlify('E3B600CCE5FF1C6155838376FD7E0330')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(5)
    print('Not joined yet...')

print('Network joined!')

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
data = {}
tmp = 0;
hum = 0;
while True:
    result = th.read()
    if result.is_valid():
        tmp = result.temperature
        hum = result.humidity
        #data['tmp'] = result.temperature
        #data['hum'] = result.humidity
    s.send(bytes([tmp,hum]))
    #s.settimeout(3.5)
    print("Packet sent: Tmp: {}, Hum: {}".format(tmp,hum))
    time.sleep(30) # wait for the tx and rx to complete
    rx_pkt = s.recv(64)   # get the packet received (if any)
    print(rx_pkt)
