import nano
import os
import RepeatedTimer
import json

import time
########################
## Variables globales ##
########################
pVerbosity = True
pExposureTime = 10.5
pFramePeriod = 11
pPrefix = ""
pMaxCubes = -1
pMaxFramesPerCube = 1000
########################

#Retorna true en caso de que la camara no haya terminado de grabar y false en el caso contrario
def polling(sensor):
    return sensor.isCapturing();


########################
##        MAIN        ##
########################
#TODO quitar sleep
time.sleep(10)
#Se inicializa, conecta y configura la camara
print("----- Script de control de la camara mediante TCP y Telnet-----")
try:
    ficheroConfig = open("parametrosCamara.json", "rt")
    configuracion = json.loads(ficheroConfig.read())
    pVerbosity =        configuracion["verbosity"]
    pExposureTime =     configuracion["exposureTime"]
    pFramePeriod =      configuracion["framePeriod"]
    pPrefix =           configuracion["prefix"]
    pMaxCubes =         configuracion["maxCubes"]
    pMaxFramesPerCube=  configuracion["maxFramesPerCube"]    
    print(f"Empleando los valores leidos del fichero de configuracion:")
except: 
    print(f"No se pudo leer el fichero de configuracion. Usando valores por defecto:")

print(f"\tverbose={pVerbosity}\n\texposureTime={pExposureTime}\n\tframePeriod={pFramePeriod}\n\tprefix: {pPrefix}\n\tmaxCubes: {pMaxCubes}\n\tmaxFramesPerCube: {pMaxFramesPerCube}")

sensor = nano.Nano(verbose=pVerbosity)
sensor.connect()
sensor.configure(exposure=pExposureTime, framePeriod=pFramePeriod)

#Se activa la captura y se almacena la respuesta para poder recuperar el directorio donde se guarda lo grabado
print("Comenzando a grabar")
captureResponse = sensor.capture(prefix=pPrefix, maxCubes=pMaxCubes, maxFramesPerCube=pMaxFramesPerCube)
directoryName = captureResponse["folder"]

rt = RepeatedTimer.RepeatedTimer(0.5, polling, sensor, directoryName)

########################
