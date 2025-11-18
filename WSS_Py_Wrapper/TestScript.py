#!/usr/bin/env python3
import clr
import configs.Loc as Loc
clr.AddReference(Loc.dllPath)

# from clr import WSSBaseCode
# from WSSBaseCode import SerialPortTransport
import logging
logger = logging.getLogger(__name__)
print("step 1 complete")
logging.basicConfig(filename='myapp.log', level=logging.INFO)
print("step 2 complete")
logger.info('statement 1')
#print(WSSBaseCode.GoFirst.bang)
print("step 3 complete")
logger.info("statement 2")
print("step 4 complete")