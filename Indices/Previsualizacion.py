#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
import sys
import wrapperIndices as wi

him = np.fromfile( sys.argv[1], np.uint16)
tamanoLinea = 640
numeroBandas = 271
numeroLineas = him.shape[0] // (tamanoLinea*numeroBandas)


him = np.reshape(np.reshape(him, (numeroLineas*numeroBandas, tamanoLinea)).T, (tamanoLinea,numeroLineas, numeroBandas))

imagen_rgb = ((him/him.max())*255).astype(np.uint16)
imagen_rgb = np.dstack((imagen_rgb[:, :, 121], imagen_rgb[:, :, 63], imagen_rgb[:, :, 36]))
imagen_rgb = (imagen_rgb*255 / imagen_rgb.max()).astype(np.uint16)

figura, subfiguras = plt.subplots(3,5)
figura.suptitle('Previsualización', fontsize=16)

subfiguras[0,0].imshow(imagen_rgb)
subfiguras[0,0].set_title('RGB')

subfiguras[0,1].imshow(wi.ndvi_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[0,1].set_title("NDVI")

subfiguras[0,2].imshow(wi.sr_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[0,2].set_title("Simple Ratio")

subfiguras[0,3].imshow(wi.evi_cube(him), cmap="RdYlGn_r", vmin=-1, vmax=1)
subfiguras[0,3].set_title("EVI")

subfiguras[0,4].imshow(wi.ztm_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[0,4].set_title("ZTM")

subfiguras[1,0].imshow(wi.gi_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[1,0].set_title("Greeness Index")

subfiguras[1,1].imshow(wi.ndre_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[1,1].set_title("NDRE")

subfiguras[1,2].imshow(wi.greenndvi_cube(him), cmap="RdYlGn_r", vmin=-1, vmax=1)
subfiguras[1,2].set_title("Green NDVI")

subfiguras[1,3].imshow(wi.srpi_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[1,3].set_title("SRPI")

subfiguras[1,4].imshow(wi.msavi_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[1,4].set_title("MSAVI")

subfiguras[2,0].imshow(wi.mcari_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[2,0].set_title("MCARI")

subfiguras[2,1].imshow(wi.mcari2_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[2,1].set_title("MCARI2")

subfiguras[2,2].imshow(wi.tcari_cube(him), cmap="RdYlGn", vmin=-1, vmax=1)
subfiguras[2,2].set_title("TCARI")

subfiguras[2,3].imshow(wi.osavi_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[2,3].set_title("OSAVI")

subfiguras[2,4].imshow(wi.ci_cube(him), cmap="RdYlGn", vmin=0, vmax=1)
subfiguras[2,4].set_title("Curvature Index")

plt.show()

plt.plot(np.array([(elem*600/271)+400 for elem in range(271)]), him[81,197,:])
plt.title("Funcion de reflectancia")
plt.show()
