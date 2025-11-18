#imports
from pythonnet import load
load("coreclr")
import clr
import configs.Loc as Loc
clr.AddReference(Loc.dllPath)

import Wss.CoreModule as WSScore # type: ignore
import datetime
import time
import portScanner
import LogSink
import Logger

logFile = Logger.logFile()


print("Connecting to Wearable Surface Stimulator Unit....\n.......\n..........")
LogSink.Log("INFO", "Connecting to WSS Unit...", logFile)

#Set Default Variables
comPort = "auto"
forcePort = False
print("Select serial port automatically? Y/N")
if input().upper() == "N":
    forcePort = True
    comPort = portScanner.runScan()
    LogSink.Log("INFO", "Serial port" + comPort + "selected.", logFile)

testMode = False
maxSetupTries = 5
JSONpath = Loc.JSONpath
#Check with user
print("test mode? Y/N")

if input().upper() == "Y":
    testMode = True
    LogSink.Log("INFO", "Test mode engaged.", logFile)

#initialize
print("Initializing WSS...")
LogSink.Log("INFO", "Begin initializing WSS unit", logFile)
if forcePort == True:
    WSS = WSScore.WssStimulationCore(comPort, JSONpath,testMode, maxSetupTries)
    LogSink.Log("INFO", "Forcing port...", logFile)
else:
    WSS = WSScore.WssStimulationCore(JSONpath,testMode, maxSetupTries)
    LogSink.Log("INFO", "Auto-detecting serial port...")
WSS.Initialize()
running = True
LogSink.Log("INFO", "WSS Connected on" + comPort, logFile)
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
