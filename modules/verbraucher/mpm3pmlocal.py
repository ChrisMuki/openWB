#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
verbrauchernr = str(sys.argv[1])
seradd = str(sys.argv[2])
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                stopbits=1, bytesize=8, timeout=1)


sdmid = int(sys.argv[3])

resp = client.read_input_registers(0x0002,4, unit=sdmid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ikwh = float(ikwh) * 10
whstring = "/var/www/html/openWB/ramdisk/verbraucher%s_wh" % (verbrauchernr)
f = open(whstring, 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x26,2, unit=sdmid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
wstring = "/var/www/html/openWB/ramdisk/verbraucher%s_watt" % (verbrauchernr)
f = open(whstring, 'w')
f = open(wstring, 'w')
f.write(str(final))
f.close()

