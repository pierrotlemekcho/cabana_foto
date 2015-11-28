#!/usr/bin/env python
import serial, sys
s = serial.Serial(port='/dev/ttyAMA0', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
j=1
while True :
    data = s.read(1)
    j = j+1
#    print(j)
#    sys.stdout.write('\ndonnes')
    if data =='\2':
         sys.stdout.write('\n===============debut=========')
    elif data =='\3' :
         sys.stdout.write('\n==============fin============')
    else:
         sys.stdout.write(data)
