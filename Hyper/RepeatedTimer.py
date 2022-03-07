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
            print("The cam is still recording")
            self.start()
        else: # Else start FTP part
            print("The cam has finished recording, the acquisition of files can begin")
            self.stop()
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False 
        #Listado de ficheros generados
        listResponse = self.args[0].listFiles(self.args[1])
        self.args[0].disconnect()
        #Se prepara FTP para recuperar lo grabado y borrarlo del almacenamiento interno
        ftpConn = ftp.FTP("10.0.65.50")
        ftpConn.login("ftpuser","ftpuser")
        #Se prepara MongoDB para almacenar los ficheros
        client = MongoClient('localhost', 27017)
        fs = gridfs.GridFS(client.test, "gridfstest")
        timestamp = time.time() #un mismo timestamp para todos los ficheros capturados a la vez
        for f in listResponse:
            if 'raw' in f["name"]: #Se guardan los ficheros en local, se almacena su contenido en mongo y se borran del sistema
                filePath = "./destino/"+f["name"][f["name"].rfind('/')+1:] 
                destFile = open(filePath, 'wb')
                ftpConn.retrbinary("RETR " + f["name"], destFile.write)
                destFile.close()
                sourceFile = open(filePath, 'rb')
                fs.put(sourceFile, filename=f["name"][f["name"].rfind('/')+1:], metadata= {"timestamp":timestamp})
                os.remove(filePath)     
            ftpConn.delete(f["name"])
            
        ftpConn.rmd(self.args[1])
        ftpConn.quit()
        print("Done")
                
