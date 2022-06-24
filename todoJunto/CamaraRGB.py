from multiprocessing import Process
import os
import cv2
import numpy as np

class CamaraRGB(Process):

    anchoImagen = 1920
    altoImagen = 1080
    fotogramasExpo = 40

    def __init__(self, rutaFichero, posicion, correccionCamara, 
                       timestampCaptura, directorioDestino, logger = None):
        super(CamaraRGB, self).__init__()
        self.rutaFichero       = rutaFichero
        self.idCamara          = self.rutaFichero.split("video")[-1]
        self.posicion          = posicion
        self.correccionCamara  = correccionCamara
        self.timestampCaptura  = timestampCaptura
        self.directorioDestino = directorioDestino
        self.logger            = logger

    def captura(self):
        streamFotogramas = cv2.VideoCapture(self.rutaFichero)
        if not (streamFotogramas.isOpened()):
            return False, np.zeros((self.anchoImagen, self.altoImagen, 3), dtype=np.uint8)
        streamFotogramas.set(cv2.CAP_PROP_FRAME_WIDTH, self.anchoImagen)
        streamFotogramas.set(cv2.CAP_PROP_FRAME_HEIGHT, self.altoImagen)
        [streamFotogramas.read() for iteracion in range(self.fotogramasExpo)]
        ret, fotograma = streamFotogramas.read()
        streamFotogramas.release()
        if ret == False: fotograma = np.zeros((anchoImagen, altoImagen, 3), dtype=np.uint8)
        return ret, fotograma

    def run(self):
        for iteracion in range(20):
            exito, fotograma = self.captura()
            if not exito: continue
            else: break
        self.logger.printINFO("camara RGB {}".format(self.rutaFichero), "Status de la captura de la : {}".format(exito))
        nombreFichero      = "{}__pos_{}__cam_{}.jpg".format(self.timestampCaptura, self.posicion, self.idCamara)
        rutaAlmacenamiento = os.path.join(self.directorioDestino, nombreFichero)
        cv2.imwrite(rutaAlmacenamiento, fotograma)
        self.logger.printINFO("camara RGB {}".format(self.rutaFichero), "Imagen capturada almacenada, terminando proceso")
