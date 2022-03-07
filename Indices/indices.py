from spectral import *
import numpy as np
import math
import time

# usage -> img = envi.open('raw_xxxx.hdr', 'rax_xxxx'); imshow(myndvi(img));


#Simple ratio
def sr(cube, r800=135, r680=126):
    return np.array([x1 / x2 for (x1, x2) in zip(cube.read_band(nir5Index), cube.read_band(red3Index))])
#Greeness Index
def gi(cube, r554, r677):
    return np.array([x1 / x2 for (x1, x2) in zip(cube.read_band(r554), cube.read_band(r677))])
#Normalized Difference Red Edge
def ndre(cube, nir5Index=135, red3Edge=122):
    return np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube.read_band(nir5Index), cube.read_band(red3Edge))])

#Normalised Difference Vegetation Index
def myndvi(cube, nir1Index=178, red5Index=126):
    return np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube.read_band(nir1Index), cube.read_band(red5Index))])

# Green Normalised Difference Vegetation Index
def greenndvi(cube, r800=135, r550=68):
    return np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(cube.read_band(r800), cube.read_band(r550))])    
#Enhanced Vegetation Index
def evi(cube, r800=135, r670=122, r475=34):
    aux1 = np.array([x1 -x2 for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])
    aux2 = np.array([x1 - (6*x2) - (7.5*x3) + 1 ] in zip(cube.read_band(r800), cube.read_band(r670), cube.read_band(r475)))    
    return np.array(2.5 * x1 / x2 for(x1, x2) in zip(aux1, aux2))
#Simple Ratio Pigment Index
def srpi(cube, r430=14, r680=126):
    return np.array([x1 / x2 for (x1,x2) in zip(cube.read_band(r430), cube.read_band(r680))])

#Modified Chlorophyll Absorption Ratio Index  
def mcari(cube, r700=135, r670=122, r550=68):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    return np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])

def mcari2(cube, r750=185, r705=137, r550=68):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r705))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r750), cube.read_band(r705))])
    return np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])    

#Transformed Chlorophyll Absorption Ratio Index
def tcari(cube, r700=135, r670=122, r550=68):
    aux1 = np.array([3*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r550))])
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(cube.read_band(r700), cube.read_band(r670))])
    return np.array([x1- (x2 *x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])

#Optimised Soil-Adjusted Vegetation Index
def osavi(cube, r800=135, r670=122):
    return np.array([(1.16 * (x1 - x2)) / (x1 + x2 + 1.16) for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])

#Zarco Tejada & Miller
def ztm(cube, r750=185, r710=140):
    return np.array([x1 / x2 for (x1, x2) in zip(aux1, aux2)])

#Improved Soil Adjusted Vegetation Index
def msavi(cube, r800=135, r670=122):
    aux1 = np.array([8*(x1 - x2) for (x1, x2) in zip(cube.read_band(r800), cube.read_band(r670))])
    aux2= np.array([((2 * x1 + 1)**2) for (x1) in cube.read_band(r800)])
    aux3 = np.array([2 * x1 for(x1) in cube.read_band(r800)])
    return np.array([ (x1 - np.sqrt(x2 - x3)) / 2 for (x1, x2, x3) in zip(aux1, aux2, aux3)])

#Double peak Index
def dpi(cube, r688=140, r710=140, r697=134):
    return np.array([(x1 * x2)/(x3**2) for (x1, x2, x3) in zip(cube.read_band(r688), cube.read_band(r710), cube.read_band(r697))])

#Curvature Index
def ci(cube, r675=122, r690=131, r683=127):
    return np.array([x1 * x2 / x3**2 for((x1, x2, x3) in zip(cube.read_band(r675), cube.read_band(r690), cube.read_band(r683))])

