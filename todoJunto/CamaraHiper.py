from multiprocessing import Process
import os
import ftplib as ftp
import json
import nano

class CamaraHiper(Process):

    def __init__(self, tiempoExposicion, periodoFotograma, maxCubos, maxFotogramasCubo, timestampCaptura,
                       directorioDestino, direccionIP, usuarioFTP, contrasenaFTP, logger = None):
        super(CamaraHiper, self).__init__()
        self.tiempoExposicion  = tiempoExposicion
        self.periodoFotograma  = periodoFotograma
        self.maxCubos          = maxCubos
        self.maxFotogramasCubo = maxFotogramasCubo
        self.timestampCaptura  = timestampCaptura
        self.directorioDestino = directorioDestino
        self.direccionIP       = direccionIP
        self.usuarioFTP        = usuarioFTP
        self.contrasenaFTP     = contrasenaFTP
        self.logger            = logger
        self.camara            = nano.Nano(verbose = False)

    def captura(self):
        try:
            self.camara.connect()
            self.camara.configure( exposure    = self.tiempoExposicion,
                                   framePeriod = self.periodoFotograma)
            directorioResultado = self.camara.capture( maxCubes         = self.maxCubos, 
                                                       maxFramesPerCube = self.maxFotogramasCubo)["folder"]
            while self.camara.isCapturing(): pass
            self.camara.disconnect()
            return directorioResultado
        except Exception as e:
            self.logger.printWARNING("Camara Hiper", "Proceso de captura Telnet fallido")
            self.logger.printERROR("Camara Hiper", e)
            return None

    def descargar(self,directorioFuente):
        try:
            conexionFTP = ftp.FTP(self.direccionIP)
            conexionFTP.login( self.usuarioFTP, self.contrasenaFTP)
            for fichero in conexionFTP.nlst(directorioFuente):
                rutaFicheroFuente = os.path.join(directorioFuente, fichero)
                if "raw" in fichero:
                    extensionFichero = ".bin"
                    if fichero.endswith(".hdr"): extensionFichero = ".hdr"
                    rutaDestino = os.path.abspath(os.path.join(self.directorioDestino, "HIM__{}{}".format(self.timestampCaptura, extensionFichero)))
                    with open(rutaDestino, "wb") as streamEscritura:
                        conexionFTP.retrbinary("RETR {}".format(rutaFicheroFuente), streamEscritura.write) 
                conexionFTP.delete(rutaFicheroFuente)
            conexionFTP.rmd(directorioFuente)
            conexionFTP.quit()
        except Exception as e:
            self.logger.printWARNING("Camara Hiper", "Proceso de descarga FTP fallido")
            self.logger.printERROR("Camara Hiper", e)
            return

    def run(self):
        directorioResultado = self.captura()
        if directorioResultado  != None: 
            self.descargar(directorioResultado)
            self.logger.printINFO("Camara Hiper", "Descarga y captura completadas, terminando proceso")
