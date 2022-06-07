import numpy as np
import math

#Simple ratio
def sr_bands(r800, r680):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r680 = np.where(r680 == 0, 1, r680)
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r800, r680)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()   

#Greeness Index
def gi_bands(r554, r677):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r677 = np.where(r677 == 0, 1, r677)
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r554, r677)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max() 

#Normalized Difference Red Edge
def ndre_bands( r780, r730):
    indiceAux = np.array([(x1 - x2) / (x1 + x2) for(x1, x2) in zip(r780, r730)])
    #Los valores resultantes de una division por 0 se sustituyen por 0
    np.nan_to_num(indiceAux, copy=False, nan=0)
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

#Normalised Difference Vegetation Index
def ndvi_bands(r800, r670):    
    indiceAux = np.array([(x1 - x2) / ((x1 + x2) | 1 ) for(x1, x2) in zip(r800, r670)])
    #Los valores resultantes de una division por 0 se sustituyen por 0
    np.nan_to_num(indiceAux, copy=False, nan=0)
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

# Green Normalised Difference Vegetation Index
def greenndvi_bands(r800, r550):
    indiceAux = np.array([(x1 - x2) / ((x1 + x2) | 1 ) for(x1, x2) in zip(r800, r550)])
    #Los valores resultantes de una division por 0 se sustituyen por 0
    np.nan_to_num(indiceAux, copy=False, nan=0)
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())     

#Enhanced Vegetation Index
def evi_bands (r800, r670, r475):
    aux1 = np.array([x1 - x2 for (x1, x2) in zip(r800, r670)])
    aux2 = np.array([x1 - (6*x2) - (7.5*x3) + 1 for (x1, x2, x3) in zip(r800, r670, r475)])
    #Para evitar divisiones por 0 se sustituyen por 1 los 0
    aux2 = np.where(aux2 == 0, 1, aux2)   
    indiceAux = np.array([2.5 * x1 / x2 for(x1, x2) in zip(aux1, aux2)])
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())    

#Simple Ratio Pigment Index
def srpi_bands(r430, r680):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r680 = np.where(r680 == 0, 1, r680)
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r430, r680)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()   

#Modified Chlorophyll Absorption Ratio Index  
def mcari_bands(r700, r670, r550):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(r700, r670)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r700, r550)])
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r670 = np.where(r670 == 0, 1, r670)
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r700, r670)])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    #Se devuelve el resultado normalizado entre -1 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())



#Modified Chlorophyll Absorption Ratio Index 2
def mcari2_bands(r750, r705, r550):
    aux1 = np.array([x1 - x2  for(x1, x2) in zip(r750, r705)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r750, r550)])
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r705 = np.where(r705 == 0, 1, r705)
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r750, r705)])
    indiceAux = np.array([x1 - (x2 * x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    #Se devuelve el resultado normalizado entre -1 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())


    
#Transformed Chlorophyll Absorption Ratio Index
def tcari_bands(r700, r670, r550):
    aux1 = np.array([3*(x1 - x2)  for(x1, x2) in zip(r700, r670)])
    aux2 = np.array([0.2*(x1 - x2)  for(x1, x2) in zip(r700, r550)])
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r670 = np.where(r670 == 0, 1, r670)
    aux3 = np.array([x1 / x2  for(x1, x2) in zip(r700, r670)])
    indiceAux = np.array([x1- (x2 *x3) for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    #Se devuelve el resultado normalizado entre -1 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())  


    
#Optimised Soil-Adjusted Vegetation Index
def osavi_bands(r800, r670):
    indiceAux = np.array([(1.16 * (x1 - x2)) / (x1 + x2 + 1.16) for (x1, x2) in zip(r800, r670)])
    #Los valores resultantes de una division por 0 se sustituyen por 0
    np.nan_to_num(indiceAux, copy=False, nan=0)
    #Se devuelve el resultado normalizado entre -1 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())  

#Zarco Tejada & Miller
def ztm_bands(r750, r710):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r710 = np.where(r710 == 0, 1, r710)
    indiceAux = np.array([x1 / x2 for (x1, x2) in zip(r750, r710)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()   
  
#Improved Soil Adjusted Vegetation Index
def msavi_bands(r800, r670):
    aux1 = np.array([8*(x1 - x2) for (x1, x2) in zip(r800, r670)])
    aux2= (2 * (r800 + 1))**2
    aux3 = 2 * r800 + 1
    indiceAux = np.array([ (x3 - np.sqrt(abs(x2 - x1))) / 2 for (x1, x2, x3) in zip(aux1, aux2, aux3)])
    #Se devuelve el resultado normalizado entre -1 y 1
    return indiceAux / abs(indiceAux.max()) if abs(indiceAux.max()) > abs(indiceAux.min()) else indiceAux / abs(indiceAux.min())   


#Double peak Index
def dpi_bands(r710, r697, r688):
    r697 = r697**2
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r697 = np.where(r697 == 0, 1, r697)
    indiceAux = np.array([(x1 * x2)/(x3) for (x1, x2, x3) in zip(r688, r710, r697)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()    

    
#Curvature Index
def ci_bands (r675, r690, r683):
    #Para evitar divisiones por 0 (poco probable pero posible) se sustituyen por 1 los 0
    r683 = np.where(r683 == 0, 1, r683)
    indiceAux = np.array([(x1 * x2) / x3 for(x1, x2, x3) in zip(r675, r690, r683)])
    #Los valores resultantes de una division por 0 se sustituyen por 1
    np.nan_to_num(indiceAux, copy=False, nan=1)
    indiceAux = np.array([x1 / x2 for(x1, x2) in zip(indiceAux, r683)])
    #Se devuelve el resultado normalizado entre 0 y 1
    return indiceAux / indiceAux.max()      
  
