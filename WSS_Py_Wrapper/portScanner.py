#!/usr/bin/env python3
import serial
from serial.tools.list_ports import comports

def runScan():
    print("Scanning for serial ports...")
    COM = "None Selected"
    for port in comports():
        print(port)
    print("Please select your COM port:")
    COM = input()
    COM = COM.upper()
    print(COM, "selected.")
    return COM