#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
import sys
import indices

him = np.fromfile( sys.argv[1], np.uint16)
tamanoLinea = 640
numeroBandas = 271
numeroLineas = him.shape[0] // (tamanoLinea*numeroBandas)

him = ((him/him.max())*255).astype(np.uint16)
him = np.reshape(np.reshape(him, (numeroLineas*numeroBandas, tamanoLinea)).T, (tamanoLinea,numeroLineas, numeroBandas))

imagen_rgb = np.dstack((him[:, :, 121], him[:, :, 63], him[:, :, 36]))
imagen_rgb = (imagen_rgb*255 / imagen_rgb.max()).astype(np.uint16)

figura, (eje1, eje2, eje3) = plt.subplots(1,3)
figura.suptitle('Previsualización', fontsize=16)

eje1.imshow(imagen_rgb)
eje1.set_title('RGB')

eje2.imshow(indices.ndvi_bands(him[:,:,160].astype(np.int16), him[:,:,71].astype(np.int16)), cmap="RdYlGn")
eje2.set_title("NDVI")

eje3.imshow(indices.sr_bands(him[:,:,160], him[:,:,71]), cmap="RdYlGn")
eje3.set_title("Simple Ratio")

plt.show()

plt.plot(np.array([(elem*600/271)+400 for elem in range(271)]), him[389,295,:])
plt.title("Funcion de reflectancia")
plt.show()
