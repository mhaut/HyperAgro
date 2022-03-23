from pymongo import MongoClient
import gridfs
import indices
from matplotlib import pyplot as plt
from spectral import *
import rasterio
import numpy as np
import time


def read_envi_hdr(pathfile):
    wavevalues = ''; metadata = {}; wlen=False
    for line in open(pathfile + '.hdr', 'r'):
        line = line.strip().strip('\n').strip('\r')
        if 'samples =' in line:                           metadata['samples'] = int(line.split('=')[1])
        elif 'lines =' in line:                           metadata['lines'] = int(line.split('=')[1])
        elif 'bands =' in line and 'default' not in line: metadata['bands'] = int(line.split('=')[1])
        elif 'data type =' in line:                       metadata['datatype'] = int(line.split('=')[1])
        elif 'interleave =' in line:                      metadata['interleave'] = line.split('=')[1]
        elif 'wavelength =' in line: wlen=True
        elif wlen and '}' in line:
            metadata['wavelength'] = wavevalues.strip().replace('{','').replace('}','').split(',')
            wlen = False
        elif wlen:                   wavevalues += line
    return metadata

def read_envi_file(pathfile, metadata):
    fd = open(pathfile+'.bin', 'rb')
    inter, lines, samples, bands = \
        metadata['interleave'], metadata['lines'], metadata['samples'], metadata['bands']
    if metadata['datatype'] == 2:    him = np.fromfile(fd, np.int16)
    elif metadata['datatype'] == 4:  him = np.fromfile(fd, np.float32)
    elif metadata['datatype'] == 5:  him = np.fromfile(fd, np.float64)
    elif metadata['datatype'] == 12: 
        him = unpack_12to16(np.fromfile(fd, np.uint16), lines*bands*samples)

    if 'bsq' in inter.lower():
        print('Convert BSQ')
        data = np.flipud(np.transpose(him.reshape(bands, samples, lines), (2, 1, 0)))
    elif 'bil' in inter.lower():
        print('Convert BIL')
        data = np.rot90(np.flipud(np.transpose(him.reshape(samples, bands, lines), (2, 0, 1))), k=2)
    elif 'bip' in inter.lower():
        print('Convert BIP')
        data = np.flipud(np.transpose(him.reshape(bands, lines, samples), (1, 2, 0)))
    return data



def unpack_12to16(packed, tamanoFinal):
    unpacked = []
    posicion = 0
    valor = 0
    iterador = iter(packed)
    elemIterPrevia = 0
    elemIterActual = 0
    media = []
    for i in range(tamanoFinal):
        start = time.time_ns()
        if (posicion == 0):
            elemIterPrevia = next(iterador)
            valor = elemIterPrevia & 0x0FFF 
        elif (posicion == 1):
            elemIterActual = next(iterador)
            valor = (elemIterPrevia & 0XF000 >> 12) | (elemIterActual & 0x00FF << 4)
            elemIterPrevia = elemIterActual
        elif (posicion == 2):
            elemIterActual = next(iterador)
            valor = (elemIterPrevia & 0xFF00 >> 8) | (elemIterActual & 0x00FF << 8)
            elemIterPrevia = elemIterActual
        else:
            valor = (elemIterPrevia & 0xFFF0 >> 4)

        posicion = (posicion + 1) % 4
        unpacked.append(valor)
        media.append(time.time_ns() - start)

    print(sum(media) / len(media))
    return np.array(unpacked)



def unpack_12to16_version2(packed):
    tiempo = time.time()
    for pos, pbits in packed:
        if   pos % 3 == 0: valor = pbits & 0x0FFF
        elif pos % 3 == 1: valor = (elemIterPrevia & 0XF000 >> 12) | (pbits & 0x00FF << 4)
        elif pos % 3 == 2: valor = (elemIterPrevia & 0xFF00 >> 8) | (elemIterActual & 0x00FF << 8)
        unpacked.append(valor)
        if   pos % 3 == 2: unpacked.append((elemIterPrevia & 0xFFF0 >> 4))
        elemIterPrevia = pbits
    print("TIEMPO", time.time() / len(packed))
    return np.array(unpacked)






client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.test, "gridfstest")

cabecera = fs.find_one({'filename': 'raw_0.hdr', 'metadata': {'timestamp': 1647973004.203551}})
him = fs.find_one({'filename': 'raw_0.bin', 'metadata': {'timestamp': 1647973004.203551}})

cabeceraFile = open('raw_0.hdr', 'wb')
cabeceraFile.write(cabecera.read())
cabeceraFile.close()

cubeFile = open('raw_0.bin', 'wb')
cubeFile.write(him.read())
cubeFile.close()

metadata = read_envi_hdr('raw_0')
data = read_envi_file('raw_0', metadata)

indice = indices.ndvi_bands(data[:, :, 180], data[:, :, 121])
print(data[:, :, 1])
plt.imshow(data[:, :, 1], cmap='binary')
plt.show()


#plt.imshow(indice, cmap='RdYlGn')
#plt.show()

