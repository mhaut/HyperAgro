import nano
import time
from pymongo import MongoClient
import gridfs
import ftplib as ftp
import os

#Leer los directorios que no se han podido recuperar del almacenamiento interno de la cam
ficheroDirectorios = open("./DirectoriosPorProcesar.txt", "rt")
rutasDirectorios = ficheroDirectorios.readlines()
ficheroDirectorios.close()
print('Directorios por recuperar', rutasDirectorios)


#Establecer conexion FTP con la camara y con mongoDB
ftpConn = ftp.FTP("10.0.65.50")
ftpConn.login("ftpuser","ftpuser")

client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.test, "gridfstest")

directoriosBorrados = []
for directorio in rutasDirectorios:
    timestamp = time.time()
    ficherosBorrar = ftpConn.nlst(directorio[:-1])
    print(ficherosBorrar)
    for fichero in ficherosBorrar:

        #Se borra cada fichero, y si es una imagen o una cabecera, se guarda
        if 'raw' in fichero:
            #Se guarda en un fichero temporal 
            filePath = "./destino/"+fichero
            ficheroDestino = open(filePath, 'wb')
            ftpConn.retrbinary("RETR " + directorio[:-1]+ '/' + fichero, ficheroDestino.write)
            ficheroDestino.close()

            #Se almacena dicho fichero en mongoDB y se borra 
            ficheroDestino = open(filePath, 'rb')
            fs.put(ficheroDestino, filename=fichero, metadata= {"timestamp":timestamp})
            ficheroDestino.close()
            os.remove(filePath)

        ftpConn.delete(directorio[:-1] +"/"+fichero)
    # Una vez vacio el directorio, se borra
    ftpConn.rmd(directorio[:-1])
    directoriosBorrados.append(directorio)

ftpConn.quit()

#Si algun directorio no se ha podido procesar, se vuelve a meter en el fichero para volver a intentarlo posteriormente
directoriosNoBorrados = list(set(rutasDirectorios) - set(directoriosBorrados))
ficheroDirectorios = open("./DirectoriosPorProcesar.txt", "wt")
ficheroDirectorios.write("")
ficheroDirectorios.close()
print(f"Directorios que no se han podido borrar: {directoriosNoBorrados}")
if (len(directoriosNoBorrados) != 0):
    ficheroDirectorios = open("./DirectoriosPorProcesar.txt", "at")
    for directorio in directoriosNoBorrados:
        ficheroDirectorios.write(directorio + "\n")
    ficheroDirectorios.close()

