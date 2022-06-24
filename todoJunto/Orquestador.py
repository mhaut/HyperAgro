import CamaraRGB
import CamaraHiper
import GestorSalidaInfo
from datetime import datetime,timedelta
import time
import os
import json
import shutil

class Orquestador:

    segundosPorDia = 86400 #24*60*60

    def __init__(self, directorioPadre, directorioDestino, directorioDestinoRGB,
                       directorioDestinoHiper, rutaCredencialesFTP, rutaCamaras,
                       rutaParametrosHiper, rgbTTL, hiperTTL, esperaDiscoLleno,
                       instanteCaptura, logger):

        self.directorioPadre        = directorioPadre
        self.directorioDestino      = directorioDestino
        self.directorioDestinoRGB   = directorioDestinoRGB
        self.directorioDestinoHiper = directorioDestinoHiper
        [os.mkdir(folder) for folder in [self.directorioPadre, self.directorioDestino, self.directorioDestinoRGB, self.directorioDestinoHiper] if not os.path.exists(folder)]

        self.rgbTTL                 = rgbTTL
        self.hiperTTL               = hiperTTL
        self.esperaDiscoLleno       = esperaDiscoLleno
        self.camarasRGB             = json.load(open(rutaCamaras, "rb"))
        self.credencialesFTP        = json.load(open(rutaCredencialesFTP, "rb"))
        self.parametrosHiper        = json.load(open(rutaParametrosHiper, "rb"))
        self.instanteCaptura        = datetime(1, 1, 1, instanteCaptura.hour, instanteCaptura.minute, instanteCaptura.second)

        self.logger = logger

    def borrarImagenes(self, directorio, ttl):
        for imagen in os.listdir(directorio):
            rutaImagen = os.path.join(directorio, imagen)
            tiempoDeltaImagen = datetime.now() - datetime.fromtimestamp(os.path.getmtime(rutaImagen))
            if tiempoDeltaImagen > ttl:
                #os.remove(os.path.join(source_folder,image))
                self.logger.printINFO("Orquestador","Fichero {} listo para ser borrado".format(imagen))

    def dormirHastaCaptura(self):
        instanteActual = datetime.now()
        tiempoDeltaDormir = (self.instanteCaptura - datetime(1,1,1, instanteActual.hour, instanteActual.minute, instanteActual.second)).total_seconds()
        if tiempoDeltaDormir < 0: tiempoDeltaDormir = self.segundosPorDia + tiempoDeltaDormir
        self.logger.printINFO("Orquestador", "Durmiento el proceso principal pid = {} durante {:.2f} horas para sincronizar la hora de captura".format(os.getpid(), tiempoDeltaDormir/3600))
        time.sleep(tiempoDeltaDormir)

    def comprobacionEspacioDisco(self):
        total, used, free = shutil.disk_usage("/")
        self.logger.printINFO("Orquestador", "Total: {} GiB - Used: {} GiB - Free: {} GiB".format((total // (2**30)), (used // (2**30)), (free // (2**30))))
        if (1 - (used / free)) < 0.20:
            self.logger.printWARNING("Orquestador", "Poco espacio libre {} GiB".format((free // (2**30))))
    def bucleEjecucion (self):
        self.dormirHastaCaptura()
        while True:
            #Borrado de imagenes cuyo timestamp de modificacion > ttl
            self.borrarImagenes(self.directorioDestinoRGB, self.rgbTTL)
            self.borrarImagenes(self.directorioDestinoHiper, self.hiperTTL)
            #Comprobacion de espacio disponible 
            self.comprobacionEspacioDisco()
            #Preparacion de los procesos
            instanteActual = datetime.now().isoformat()
            camaras = [CamaraRGB.CamaraRGB(camara["path"], camara["pos"], camara["correction"], instanteActual, self.directorioDestinoRGB, self.logger) for camara in self.camarasRGB]
            camaras.append(CamaraHiper.CamaraHiper(self.parametrosHiper["exposureTime"], self.parametrosHiper["framePeriod"], self.parametrosHiper["maxCubes"],                                           
                                                   self.parametrosHiper["maxFramesPerCube"], instanteActual, self.directorioDestinoHiper, self.credencialesFTP["dirIP"], 
                                                   self.credencialesFTP["user"], self.credencialesFTP["password"], self.logger))
            #Ejecucion paralela de la captura de todas las camaras
            self.logger.printINFO("Orquestador", "{} procesos preparados para realizar capturas paralelas".format(len(camaras)))
            [camara.start() for camara in camaras]
            #Dormir hasta que haya que capturar
            self.logger.printINFO("Orquestador", "Durmiento al proceso principal pid = {} hasta la siguiente captura ({:.2f} horas)".format(os.getpid(), self.segundosPorDia/3600))
            time.sleep(self.segundosPorDia)


if __name__ == '__main__':
    directorioPadre     = os.path.dirname(os.path.abspath(__file__))
    directorioDestino   = os.path.join(directorioPadre, "saving")
    directorioRGB       = os.path.join(directorioDestino, "rgb")
    directorioHiper     = os.path.join(directorioDestino, "hiper")
    rutaCredencialesFTP = os.path.join(directorioPadre, "credencialesFTP")
    rutaCamaras         = os.path.join(directorioPadre, "camarasJSON")
    rutaParametrosHiper = os.path.join(directorioPadre, "parametrosHiper")
    rgbTTL = timedelta(days=30)
    hiperTTL = timedelta(days=7)
    esperaDiscoLleno = timedelta(hours=2)
    instanteCaptura = datetime(1,1,1, 12, 30, 00)
    logger = GestorSalidaInfo.GestorSalidaInfo()

    orquestador = Orquestador( directorioPadre, directorioDestino, directorioRGB, 
                               directorioHiper, rutaCredencialesFTP, rutaCamaras, 
                               rutaParametrosHiper, rgbTTL, hiperTTL,
                               esperaDiscoLleno, instanteCaptura, logger)
    orquestador.bucleEjecucion()
