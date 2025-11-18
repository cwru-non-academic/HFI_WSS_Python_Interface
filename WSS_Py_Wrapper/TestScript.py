from pythonnet import load
load("coreclr")
import clr
import configs.Loc as Loc
clr.AddReference(Loc.dllPath)
import Wss.CoreModule as WSScore # type: ignore

import LogSink
import Logger

test = Logger.logFile()
LogSink.Log("Error", "message", test)
print("looks okay so far...")
