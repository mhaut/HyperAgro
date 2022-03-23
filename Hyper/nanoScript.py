import nano
import time
from pymongo import MongoClient
import gridfs
import ftplib as ftp
import os
import RepeatedTimer

#Retorna true en caso de que la camara no haya terminado de grabar y false en el caso contrario
def polling(sensor):
    return sensor.isCapturing();


#MAIN
#Se inicializa, conecta y configura la camara
sensor = nano.Nano(verbose=True)
sensor.connect()
sensor.configure(exposure=10.5, framePeriod=11)

#Se activa la captura y se almacena la respuesta para poder recuperar el directorio donde se guarda lo grabado
captureResponse = sensor.capture(prefix="HaciendoPruebas", maxCubes=1, maxFramesPerCube=500)

directoryName = captureResponse["folder"]


rt = RepeatedTimer.RepeatedTimer(0.1, polling, sensor, directoryName)

#Se puede seguir haciendo tareas (si hay)
