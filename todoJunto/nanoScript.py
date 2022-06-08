import os
import json
import time

import nano
import RepeatedTimer
import utils
########################
## Variables globales ##
########################
pVerbosity = True
pExposureTime = 10.5
pFramePeriod = 11
pPrefix = ""
pMaxCubes = -1
pMaxFramesPerCube = 1000


TARGET_DATETIME_TIME = "20:30:00" # HORA DEL DIA A LA QUE SE REALIZA LA CAPTURA (formato 24 horas)
########################





#Retorna true en caso de que la camara no haya terminado de grabar y false en el caso contrario
def polling(sensor):
    return sensor.isCapturing();

def captura():
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
        ficheroConfig.close()    
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
    
    #Se activa la transferencia de los ficheros
    rt = RepeatedTimer.RepeatedTimer(1, polling, sensor, directoryName)



########################
##        MAIN        ##
########################

#captura()
#exit()
while True:
    # Esperamos hasta la siguiente hora target antes de la siguiente captura
    utils.waitTillTargetTime(TARGET_DATETIME_TIME)
    # Una vez despierta, ejecuta la funcionalidad
    captura()

########################
