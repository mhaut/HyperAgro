from threading import Timer
import nano
import time
from pymongo import MongoClient
import gridfs
import ftplib as ftp
import os

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer         = None
        self.interval       = interval
        self.function       = function
        self.args           = args
        self.kwargs         = kwargs
        self.is_running     = False
        self.start()

    def _run(self):
        self.is_running = False
        # If the cam is still recording, restart the timer
        if self.function(self.args[0]):
            print("La camara sigue grabando")
            self.start()
        else: # Else start FTP part
            print(f"La camara ha terminado de grabar, se pueden recuperar los ficheros del directorio {self.args[1]}")
            self.args[0].disconnect()
            self.stop()
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):

        self._timer.cancel()
        self.is_running = False 
        #Se prepara FTP para recuperar lo grabado y borrarlo del almacenamiento interno
        try:    
            ftpConn = ftp.FTP("10.0.65.50")
            ftpConn.login("ftpuser","ftpuser")
            #Se prepara MongoDB para almacenar los ficheros
            client = MongoClient('localhost', 27017)
            fs = gridfs.GridFS(client.test, "gridfstest")
            timestamp = time.time() #un mismo timestamp para todos los ficheros capturados a la vez
            listResponse = ftpConn.nlst(self.args[1]) # Listado de ficheros generados
            print(f"ficheros por procesar:{listResponse}")
            for f in listResponse:
                if 'raw' in f: #Se guardan los ficheros en local, se almacena su contenido en mongo y se borran del sistema
                    filePath = "./destino/" + f 
                    destFile = open(filePath, 'wb')
                    ftpConn.retrbinary("RETR " + self.args[1] + "/" + f, destFile.write)
                    destFile.close()
                    sourceFile = open(filePath, 'rb')
                    fs.put(sourceFile, filename=f, metadata= {"timestamp":timestamp})
                    os.remove(filePath)   
                ftpConn.delete(self.args[1] + "/" + f) #Se borra el fichero leido de la camara
                
            ftpConn.rmd(self.args[1]) #Se borra el directorio vaciado de la camara
            ftpConn.quit() #Se cierra la conexion
        except: 
            # Si la conexion falla se guarda en un fichero la ruta del directorio para procesarlo en otro momento
            print("################ERROR################")
            errorFile = open("DirectoriosPorProcesar.txt", "at")
            errorFile.write(self.args[1]+"\n")
            errorFile.close()
        print("Done")
                
