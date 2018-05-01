from machine import SD
import os
import time

#Execise 2
def exercise2():
    file_path = '/flash/log/'
    file_name = "log.csv"

with open(file_path+file_name, 'w') as f:
    f.write("start\n")
    str = "Joint ICTP-IAEA School on LoRa Enabled Radiation and Environmental Monitoring Sensors\n" * 10
    f.write(str)
    f.write("finish\n")
with open(file_path+file_name, 'r') as f:
    print(f.readall())

# # VERSION 1
# # Writing a file in /flash folder
# file_path = '/flash/log'
#
# try:
#     os.listdir('/flash/log')
#     print('/flash/log file already exists.')
# except OSError:
#     print('/flash/log file does not exist. Creating it ...')
#     os.mkdir('/flash/log')
#
# name = '/my_first_file.log'
#
# # Writing
# with open(file_path + name, 'w') as f:
#     f.write('Testing write operations in a file.')
#
# # Reading
# with open(file_path + name, 'r') as f:
#     print(f.readall())
exercise2()
