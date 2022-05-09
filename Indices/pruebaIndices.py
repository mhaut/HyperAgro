import numpy as np
import indices
import multiprocessing
import matplotlib.pyplot as plt
import time
from pymongo import MongoClient
import gridfs
from spectral import *
def preparar_batches(him):
    nCoresDisponibles = multiprocessing.cpu_count() - 1
    if nCoresDisponibles == 0: nCoresDisponibles += 1 #Por si acaso solo se tiene un core    
    batches = []
    if (len(him) // nCoresDisponibles) % 3 != 0:
        valoresFaltantes = len(him) % nCoresDisponibles
        batch_size = (len(him) // nCoresDisponibles) + valoresFaltantes
        batch_reminder_size = batch_size - ((nCoresDisponibles - 1) * valoresFaltantes) 
        for i in range(nCoresDisponibles - 1):
            batches.append(him[i*batch_size:(i+1)*batch_size])
        batches.append(him[-batch_reminder_size:])
    else:
        batch_size = (len(him) // nCoresDisponibles)
        for i in range(nCoresDisponibles):
            batches.append(him[i*batch_size:(i+1)*batch_size])

    print(f"Numero de batches -> {nCoresDisponibles}\nTamano de batch -> {batch_size}")
    if (len(him) // nCoresDisponibles) % 3 != 0: print(f"Tamano del ultimo batch -> {batch_reminder_size}")  
    return batches

def unpack_12to16_version2(packed):
    unpacked = []
    for pos, pbits in enumerate(packed):
        if   pos % 3 == 0: unpacked.append(pbits & 0x0FFF)
        elif pos % 3 == 1: unpacked.append(((elemIterPrevia & 0XF000) >> 12) | ((pbits & 0x00FF) << 4))
        elif pos % 3 == 2: 
            unpacked.append(((elemIterPrevia & 0xFF00) >> 8) | ((pbits & 0x00F) << 8))
            unpacked.append((pbits & 0xFFF0) >> 4)
        elemIterPrevia = pbits

    print(f"El Proceso-{multiprocessing.current_process()._identity} ha terminado")
    return np.array(unpacked)


##################
#####  MAIN  #####
##################

#Cargamos la imagen
client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.test, "gridfstest")

cabecera = fs.find({'filename': 'raw_0.hdr'}).sort("uploadDate", -1).limit(1) 
cabeceraFile = open('raw_0.hdr', 'wb')
cabeceraFile.write(cabecera.next().read())
cabeceraFile.close()

him = fs.find({'filename': 'raw_0.bin'}).sort("uploadDate", -1).limit(1) 
him = np.frombuffer(him.next().read(), np.uint16)
nLineas = len(him) /(271*640)
print(f'Numero de valores de la imagen hiperespectral {len(him)}')

#Preparamos los batchs
batches = preparar_batches(him)
result_list = []

#Procesamos los batchs en paralelo y mostramos el resultado
with multiprocessing.Pool(len(batches)) as p:
    tiempo = time.time()
    result_list = p.map(unpack_12to16_version2, batches)

print(f'Tiempo tardado en desempaquetar {time.time()-tiempo}')
print(len(result_list))

cubeFile = open('desempaquetado.bin', 'wb')

for sublist in result_list:
    for pixel in sublist:
        cubeFile.write(pixel.astype('uint16'))
cubeFile.close()
data = envi.open("raw_0.hdr", "desempaquetado.bin")
print(data.shape)

#A partir de aqui son pruebas

sr_data = indices.sr_cube(data)
sr_data = sr_data / sr_data.max()
plt.imshow(sr_data)
plt.show()
dataPack = np.dstack([data.read_band(121), data.read_band(63), data.read_band(36)])
dataPack = dataPack * 255 // dataPack.max()
print(dataPack.shape)
plt.imshow(dataPack)
plt.show()
nLineasDecomp = nLineas * 16 // 12
bandInfo = np.squeeze(data[int(nLineasDecomp // 2), 320, :])
bandInfo = bandInfo/ max(bandInfo)
plt.plot(data.bands.centers, bandInfo, label="x = 320 y= 1/2")

bandInfo = np.squeeze(data[int(nLineasDecomp*2 // 3), 500, :])
bandInfo = bandInfo/ max(bandInfo)
plt.plot(data.bands.centers, bandInfo, label="x = 500 y= 2/3")

bandInfo = np.squeeze(data[int(nLineasDecomp // 3), 200, :])
bandInfo = bandInfo/ max(bandInfo)
plt.plot(data.bands.centers, bandInfo, label="x = 200 y= 1/3")

plt.xlabel("Longitud de onda (nm)")
plt.ylabel("Reflectancia")
plt.legend(loc='upper right')
plt.show()
