from pythonnet import load
load("coreclr")

import clr
import WSS_Loader  # Use the shared loader
from WSS_Loader import LogType
from System import Activator
import Logger

# Global log file instance
_global_logFile = None

def set_global_logfile(logFile):
	"""Set the global log file instance"""
	global _global_logFile
	_global_logFile = logFile

def Log(level, message, logFile=None):
	"""Log a message. If logFile is not provided, uses the global log file."""
	# Use provided logFile or fall back to global
	log_file = logFile if logFile is not None else _global_logFile

	if log_file is None:
		print(f"Warning: No log file available. Message: [{level}] {message}")
		return

	if level.upper() == "WARN":
		# Call static methods on the LogType
		LogType.GetMethod("Warn").Invoke(None, [message])
		log_file.entry("WARN:  " + message)

	elif level.upper() == "ERROR":
		LogType.GetMethod("Error").Invoke(None, [message])
		log_file.entry("ERROR:  " + message)

	else:
		log_file.entry("INFO:  "+ message)

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