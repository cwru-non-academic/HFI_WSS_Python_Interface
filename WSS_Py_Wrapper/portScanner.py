#!/usr/bin/env python3
import clr
#I'll make a config later but for now set the below path to match where YOUR WSS_Core_Interface.dll file is ;)
clr.AddReference(r'C:\Users\shs120\HFI_WSS_Python_Interface\Cs_Libraries\WSS_Core_Interface.dll')
from clr import WSSBaseCode

import sys
import serial
from serial.tools.list_ports import comports

print("Scanning for serial ports...")
COM = "None Selected"
for port in comports():
    print(port)
print("Please select your COM port:")
COM = input()
COM = COM.upper()
print(COM, "selected.\t Connecting...")

ser = serial.Serial(COM)