#!/usr/bin/env python3
import clr
import configs.Loc as Loc
from clr import CoreModule
clr.AddReference(Loc.dllPath)


def sink(level, message):
    match level:
        case CoreModule.LogLevel.Info:
            Log.info(message)
        case CoreModule.LogLevel.Warning:
            Log.warning(message)
        case CoreModule.LogLevel.Error:
            Log.error(message)