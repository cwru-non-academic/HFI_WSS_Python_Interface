#!/usr/bin/env python3
#!/usr/bin/env python3
import clr
import configs.Loc as Loc
clr.AddReference(Loc.dllPath)

import Wss.CoreModule as CoreModule # type: ignore
import time
import portScanner



# def sink(level, message):
#         match level:
#             case CoreModule.LogLevel.Info:
#                 pass
#             case CoreModule.LogLevel.Warning:
#                 print("Warning: " + message)
#             case CoreModule.LogLevel.Error:
#                 print("Error: " + message)

#deligate = action[CoreModule.LogLevel, str](sink)
#CoreModule.Log.SetSink(deligate)


print("Connecting to Wearable Surface Stimulator Unit....\n.......\n..........")


#Set Default Variables
comPort = "auto"
forcePort = False
print("Select COM port automatically? Y/N")
if input().upper() == "N":
    forcePort = True
    comPort = portScanner.runScan()

testMode = False
maxSetupTries = 5
JSONpath = Loc.JSONpath
#Check with user
print("test mode? Y/N")

if input().upper() == "Y":
    testMode = True

#initialize
print("Initializing WSS...")
if forcePort == True:
    WSS = CoreModule.WssStimulationCore(comPort, JSONpath,testMode, maxSetupTries)
else:
    WSS = CoreModule.WssStimulationCore(JSONpath,testMode, maxSetupTries)
WSS.Initialize()
running = True
print("successfully connected to WSS on", comPort, ".\nInstructions:\n\tTo close connection, enter 'Q'.\n\tTo restart, enter 'R'.\n\tTo load a new configuration file, enter 'N'.\n\tFor analog stimulation, enter 'A'.")


while running==True:
    WSS.Tick()
    grab = input().upper()
    if grab == 'Q':
        WSS.Shutdown()
        running = False
        print("WSS shutdown complete.")
    elif grab == 'R':
        WSS.Shutdown()
        print("WSS shutdown.\nRestarting...")
        WSS.Initialize()
    elif grab == 'N':
        WSS.LoadConfigFile()
        print("New config file loaded.")
    elif grab == 'A':
        StimLoc = input("Enter stimulation location (e.g., 'A1', 'B2', etc.): ").upper()
        PW = input("Enter pulse width (in microseconds): ")
        amp = input("Enter amplitude (in mA): ")
        IPI = input("Enter inter-pulse interval (in ms): ")
        WSS.StimulateAnalog(StimLoc, int(PW), int(amp), int(IPI))
    time.sleep(2)
