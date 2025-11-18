import serial
from serial.tools.list_ports import comports

def runScan():
    print("Scanning for serial ports...")
    COM = "None Selected"
    for port in comports():
        print(port)
    print("Please select your serial port:")
    COM = input()
    print(COM, "selected.")
    return COM
