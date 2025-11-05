#!/usr/bin/env python3
import clr
#I'll make a config later but for now set the below path to match where YOUR WSS_Core_Interface.dll file is ;)
clr.AddReference(r'C:\Users\shs120\HFI_WSS_Python_Interface\Cs_Libraries\WSS_Core_Interface.dll')
print("step 1 complete")
from clr import WSSBaseCode
#from WSSBaseCode import GoFirst
print("step 2 complete")
print(WSSBaseCode.GoFirst.bang)
print("step3 complete")