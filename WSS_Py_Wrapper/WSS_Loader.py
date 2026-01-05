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
from System import AppDomain, Type, Activator

# Set the base directory for assembly resolution
AppDomain.CurrentDomain.SetData("APP_CONTEXT_BASE_DIRECTORY", dll_dir)

# Load System.IO.Ports using Assembly.LoadFile (absolute path)
ports_dll_path = os.path.join(dll_dir, "System.IO.Ports.dll")
Assembly.LoadFile(ports_dll_path)

# Load the main assembly
assembly = Assembly.LoadFile(Loc.dllPath)

# Get the types you need
WssStimulationCoreType = assembly.GetType("WssStimulationCore")
LogType = assembly.GetType("Log")