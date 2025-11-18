from pythonnet import load
load("coreclr")

import clr
import configs.Loc as Loc
clr.AddReference(Loc.dllPath)
import Wss.CoreModule as WSScore # type: ignore
import Logger

def Log(level, message, logFile):
	if level.upper() == "WARN":
		WSScore.Log.Warn(message)
		logFile.entry("WARN:  " + message)

	elif level.upper() == "ERROR":
		WSScore.Log.Error(message)
		logFile.entry("ERROR:  " + message)

	else:
		logFile.entry("INFO:  "+ message)

# def sink(level, message):
#     match level:
#         case WSScore.LogLevel.Info:
#              WSScore.Log.info(message)
#              print("info received debug msg")
#         case WSScore.LogLevel.Warning:
#             WSScore.Log.warning(message)
#             print("warning received debug msg")
#         case WSScore.LogLevel.Error:
#             WSScore.Log.error(message)
#             print("error received debug msg")
