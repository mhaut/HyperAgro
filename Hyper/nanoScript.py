import nano
import time
from pymongo import MongoClient
import gridfs
import ftplib as ftp
import os
import RepeatedTimer

def polling(sensor):
    return sensor.isCapturing();


sensor = nano.Nano(verbose=True)
sensor.connect()
sensor.configure(exposure=10.5, framePeriod=11)

captureResponse = sensor.capture(prefix="HaciendoPruebas", maxCubes=1, maxFramesPerCube=10)

directoryName = captureResponse["folder"]

rt = RepeatedTimer.RepeatedTimer(0.1, polling, sensor, directoryName)

#Keep doing stuff...
    
