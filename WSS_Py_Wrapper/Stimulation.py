#imports
from pythonnet import load
load("coreclr")
import clr
import sys
import os
import configs.Loc as Loc

# Add the Cs_Libraries directory to the path
dll_dir = os.path.dirname(Loc.dllPath)
sys.path.append(dll_dir)

# Set up CLR assembly resolution
clr.AddReference("System")
from System.Reflection import Assembly
from System import AppDomain, Type, String, Boolean, Int32

# Set the base directory for assembly resolution
AppDomain.CurrentDomain.SetData("APP_CONTEXT_BASE_DIRECTORY", dll_dir)

# Load required security assemblies first (needed for Newtonsoft.Json compatibility with .NET 9)
security_assemblies = [
    os.path.join(dll_dir, "System.Security.Permissions.dll"),
    os.path.join(dll_dir, "System.Security.AccessControl.dll"),
    os.path.join(dll_dir, "System.Security.Principal.Windows.dll")
]

for sec_assembly in security_assemblies:
    if os.path.exists(sec_assembly):
        try:
            Assembly.LoadFile(sec_assembly)
        except Exception as e:
            print(f"Warning: Could not load {os.path.basename(sec_assembly)}: {e}")

# Load the main assembly using LoadFile
assembly = Assembly.LoadFile(Loc.dllPath)

# Get the WssStimulationCore type from the assembly
WssStimulationCoreType = assembly.GetType("WssStimulationCore")
LogType = assembly.GetType("Log")

import datetime
import time
import portScanner
import LogSink
import Logger
from System import Action

logFile = Logger.logFile()

# Set the global log file so LogSink.Log can be called with 2 parameters
LogSink.set_global_logfile(logFile)

# Register the Python log sink with the C# Log class if available
if LogType is not None:
    # Create a .NET Action delegate from the Python LogSink.Log function
    logSinkDelegate = Action[str, str](LogSink.Log)

    # Try to set the LogSink property/field
    logSinkField = LogType.GetField("LogSink")
    if logSinkField is not None:
        logSinkField.SetValue(None, logSinkDelegate)
    else:
        # Try as a method
        setLogSinkMethod = LogType.GetMethod("SetLogSink")
        if setLogSinkMethod is not None:
            setLogSinkMethod.Invoke(None, [logSinkDelegate])

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


# Try creating instance
try:
    if forcePort == True:
        # Get constructor with 4 parameters: String, String, Boolean, Int32
        ctor = WssStimulationCoreType.GetConstructor([String, String, Boolean, Int32])
        # Convert Python values to .NET types explicitly
        WSS = ctor.Invoke([String(comPort), String(JSONpath), Boolean(testMode), Int32(maxSetupTries)])
        LogSink.Log("INFO", "Forcing port...", logFile)
    else:
        # Get constructor with 3 parameters: String, Boolean, Int32
        ctor = WssStimulationCoreType.GetConstructor([String, Boolean, Int32])
        # Convert Python values to .NET types explicitly
        WSS = ctor.Invoke([String(JSONpath), Boolean(testMode), Int32(maxSetupTries)])
        LogSink.Log("INFO", "Auto-detecting serial port...")
except Exception as e:
    print(f"Failed to create instance: {e}")
    print("Trying without maxSetupTries...")
    try:
        if forcePort == True:
            # Get constructor with 3 parameters: String, String, Boolean
            ctor = WssStimulationCoreType.GetConstructor([String, String, Boolean])
            if ctor is not None:
                WSS = ctor.Invoke([String(comPort), String(JSONpath), Boolean(testMode)])
            else:
                print("Constructor not found!")
                sys.exit(1)
        else:
            # Get constructor with 2 parameters: String, Boolean
            ctor = WssStimulationCoreType.GetConstructor([String, Boolean])
            if ctor is not None:
                WSS = ctor.Invoke([String(JSONpath), Boolean(testMode)])
            else:
                print("Constructor not found!")
                sys.exit(1)
    except Exception as e2:
        print(f"Also failed: {e2}")
        import sys
        sys.exit(1)

try:
    WSS.Initialize()
    print("\nWSS Initialized successfully!")
except Exception as e:
    print(f"\nError during WSS initialization: {e}")
    if "PlatformNotSupportedException" in str(type(e).__name__) or "only supported on Windows" in str(e):
        print("\n" + "="*60)
        print("PLATFORM ISSUE DETECTED")
        print("="*60)
        print("System.IO.Ports serial port enumeration is not supported on macOS.")
        print("\nPossible solutions:")
        print("1. Run this application on Windows")
        print("2. Recompile WSS_Core_Interface.dll with macOS-compatible serial")
        print("   port handling (using /dev/tty.* or /dev/cu.* devices)")
        print("3. Check if the C# code has a test/mock mode that bypasses")
        print("   serial port initialization")
        print("="*60)
    sys.exit(1)

print("\nWSS Initialized successfully!")
print("\nCommands:")
print("  Q - Quit/Shutdown")
print("  R - Restart")
print("  N - Load new config file")
print("  A - Analog stimulation")
print()

running = True
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