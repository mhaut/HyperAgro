from spectral import *
import numpy as np
import math
from matplotlib import pyplot as plt 


#Simple ratio
def sr_cube(cube, r800=135, r680=126):
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r680))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def sr_bands(r800, r680):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1
    r680 = np.where(r680 == 0, 1, r680)
    print("Reflectancia de una hoja roja:",r680[389,295],r800[389,295] )
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r800, r680)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()   


#Greeness Index
def gi_cube(cube, r554=69, r677=125):
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(cube.read_band(r554), cube.read_band(r677))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def gi_bands(r554, r677):
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r554, r677)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min()) 


#Normalized Difference Red Edge
def ndre_cube(cube, nir5Index=135, red3Edge=122):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube.read_band(nir5Index), cube.read_band(red3Edge))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def ndre_bands( nir5, red3):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(nir5Index, red3Edge)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     


#Normalised Difference Vegetation Index
def ndvi_cube(cube, r800=180, r670=121):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube[:,:,r800], cube[:,:,r670])])
    np.nan_to_num(indiceAux, copy=False, nan=0)
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def ndvi_bands(r800, r670):    
    indiceAux = np.array([(x1 - x2) / ((x1 + x2) | 1 ) for(x1, x2) in zip(r800, r670)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     


# Green Normalised Difference Vegetation Index
def greenndvi_cube(cube, r800=135, r550=68):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube.read_band(r800), cube.read_band(r550))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def greenndvi_bands(r800, r550):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(r800, r550)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

#Enhanced Vegetation Index
def evi_cube(cube, r800=135, r670=122, r475=34):
    aux1 = np.array([x1 - x2 for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])
    aux2 = np.array([x1 - (6*x2) - (7.5*x3) + 1 for (x1, x2, x3) in zip(cube.read_band(r800), cube.read_band(r670), cube.read_band(r475))])    
    indiceAux = np.array([2.5 * x1 / x2 for(x1, x2) in zip(aux1, aux2)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def evi_bands (r800, r670, r475):
    aux1 = r800 - r670
    aux2 = r800 - (6*r670) - (7.5*r475) + 1
    return 2.5 * aux1 / aux2


#Simple Ratio Pigment Index
def srpi_cube(cube, r430=14, r680=126):
    return np.array([x1 / x2 for (x1,x2) in zip(cube.read_band(r430), cube.read_band(r680))])

def srpi_bands(r430, r680):
    return r430/r680

#Modified Chlorophyll Absorption Ratio Index  
def mcari_cube(cube, r700=135, r670=122, r550=68):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())

def mcari_bands(r700, r670, r550):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(r700, r670)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r700, r550)])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r700, r670)])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())


def mcari2_cube(cube, r750=185, r705=137, r550=68):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r705))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r705))])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())

def mcari2_bands(r750, r705, r550):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(r750, r705)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r750, r550)])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r750, r705)])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())  

#Transformed Chlorophyll Absorption Ratio Index
def tcari_cube(cube, r700=135, r670=122, r550=68):
    aux1 = np.array([3*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    indiceAux = np.array([x1- (x2 *x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def tcari_bands(r700, r670, r550):
    aux1 = np.array([3*(x1 - x2)  for(x1, x2) in zip(r700, r670)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r700, r550)])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r700, r670)])
    indiceAux = np.array([x1- (x2 *x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())  


#Optimised Soil-Adjusted Vegetation Index
def osavi_cube(cube, r800=135, r670=122):
    indiceAux = np.array([(1.16 * (x1 - x2)) / (x1 + x2 + 1.16) for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

def osavi_bands(r800, r670):
    indiceAux = np.array([(1.16 * (x1 - x2)) / (x1 + x2 + 1.16) for (x1, x2) in zip(r800, r670)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    


#Zarco Tejada & Miller
def ztm_cube(cube, r750=185, r710=140):
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(cube.read_band(r750), cube.read_band(r710))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    

def ztm_bands(r750, r710):
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r750, r710)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    



#Improved Soil Adjusted Vegetation Index
def msavi_cube(cube, r800=135, r670=122):
    aux1 = np.array([8*(x1 - x2) for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])
    aux2= (2 * (cube.read_band(r800) + 1))**2
    aux3 = 2 * cube.read_band(r800) + 1
    indiceAux = np.array([ (x3 - np.sqrt(x2 - x1)) / 2 for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    

def msavi_bands(r800, r670):
    aux1 = np.array([8*(x1 - x2) for (x1, x2) in zip(r800, r670)])
    aux2= (2 * (r800 + 1))**2
    aux3 = 2 * r800 + 1
    indiceAux = np.array([ (x3 - np.sqrt(x2 - x1)) / 2 for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())   


#Double peak Index
def dpi_cube(cube, r688=140, r710=140, r697=134):
    indiceAux = np.array([(x1 * x2)/(x3) for (x1, x2, x3) in zip(cube.read_band(r688), cube.read_band(r710), cube.read_band(r697))])
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(indiceAux, cube.read_band(r697))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    

def dpi_bands(r688, r710, r697):
    indiceAux = np.array([(x1 * x2)/(x3) for (x1, x2, x3) in zip(r688, r710, r697)])
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(indiceAux, r697)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())      


#Curvature Index
def ci_cube(cube, r675=122, r690=131, r683=127):
    indiceAux = np.array([(x1 * x2) / x3 for(x1, x2, x3) in zip(cube.read_band(r675), cube.read_band(r690), cube.read_band(r683))])
    indiceAux = np.array([x1 / x2 for(x1, x2) in zip(indiceAux, cube.read_band(r683))])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    

def ci_bands (r675, r690, r683):
    indiceAux = np.array([(x1 * x2) / x3 for(x1, x2, x3) in zip(r675, r690, r683)])
    indiceAux = np.array([x1 / x2 for(x1, x2) in zip(indiceAux, r683)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    
  


#img = envi.open('raw_2000.hdr', 'raw_2000')

#indice = ndvi_bands(img.read_band(180), img.read_band(121))

#print('Min: ', indice.min(), ' Max: ', indice.max())
#plt.imshow(indice, cmap='RdYlGn')
#plt.show()

