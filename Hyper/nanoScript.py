import nano
import time
from pymongo import MongoClient
import gridfs
import ftplib as ftp
import os

#Grabar
sensor = nano.Nano(verbose=True)
sensor.connect()

#TODO Determinar valores optimos 
sensor.configure(exposure=10.5, framePeriod=11)

captureResponse = sensor.capture(prefix="HaciendoPruebas", maxCubes=1, maxFramesPerCube=10)

time.sleep(2) # Como poco framePeriod*0.0001 * maxCubes * maxFramesPerCube

directoryName = captureResponse["folder"]

listResponse = sensor.listFiles(directoryName)
sensor.disconnect()

#Se prepara FTP para recuperar lo grabado y borrarlo del almacenamiento interno
ftp = ftp.FTP("10.0.65.50")
ftp.login("ftpuser","ftpuser")
#Se prepara MongoDB para almacenar los ficheros
client = MongoClient()
client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.test, "gridfstest")
timestamp = time.time() #un mismo timestamp para todos los ficheros capturados a la vez
for f in listResponse:
    if 'raw' in f["name"]: #TODO Meter a mongo los bytes leidos directamente
        filePath = "./destino/"+f["name"][f["name"].rfind('/')+1:] 
        destFile = open(filePath, 'wb')
        ftp.retrbinary("RETR " + f["name"], destFile.write)
        destFile.close()
        os.remove(filePath) 
        
        sourceFile = open(filePath, 'rb')
        fs.put(sourceFile, filename=f["name"][f["name"].rfind('/')+1:], metadata= {"timestamp":timestamp})

    ftp.delete(f["name"])


ftp.rmd(directoryName)

ftp.quit()



    



