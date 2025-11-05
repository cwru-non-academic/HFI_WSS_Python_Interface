import clr
clr.AddReference(r'C:\Users\shs120\WSSCoreInterface\bin\Debug\net48\WSS_Core_Interface.dll')
print("step 1 complete")
from clr import WSSBaseCode
#from WSSBaseCode import GoFirst
print("step 2 complete")
print(WSSBaseCode.GoFirst.bang)
print("step3 complete")