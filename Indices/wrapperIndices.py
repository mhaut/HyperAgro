import numpy as np
import indices as i

#Simple ratio
def sr_cube(him, r800=169, r680=118):
    return i.sr_bands(him[:,:,r800], him[:,:,r680])

#Greeness Index
def gi_cube(him, r554=65, r677=117):
    return i.gi_bands(him[:,:,r554], him[:,:,r677])

#Normalized Difference Red Edge
def ndre_cube(him, r780=160, r730=140):
    #Hay que castear los valores a tipos con signo
    return i.ndre_bands(him[:,:,r780].astype(np.int16), him[:,:,r730].astype(np.int16))

#Normalised Difference Vegetation Index
def ndvi_cube(him, r800=169, r670=114):
    #Hay que castear los valores a tipos con signo
    return i.ndvi_bands(him[:,:,r800].astype(np.int16), him[:,:,r670].astype(np.int16))

# Green Normalised Difference Vegetation Index
def greenndvi_cube(him, r800=135, r550=64):
    #Hay que castear los valores a tipos con signo
    return i.greenndvi_bands(him[:,:,r800].astype(np.int16), him[:,:,r550].astype(np.int16)) 

#Enhanced Vegetation Index
def evi_cube(him, r800=169, r670=114, r475=31):
    return i.evi_bands(him[:,:,r800].astype(np.int16), him[:,:,r670].astype(np.int16), him[:,:,r475].astype(np.int16))

#Simple Ratio Pigment Index
def srpi_cube(him, r430=13, r680=118):
    return i.srpi_bands(him[:,:,r430], him[:,:,r680])

#Modified Chlorophyll Absorption Ratio Index  
def mcari_cube(him, r700=127, r670=114, r550=64):
    return i.mcari_bands(him[:,:,r700].astype(np.int16), him[:,:,r670].astype(np.int16), him[:,:,r550].astype(np.int16))

#Modified Chlorophyll Absorption Ratio Index 2
def mcari2_cube(him, r750=148, r705=129, r550=64):
    return i.mcari_bands(him[:,:,r750].astype(np.int16), him[:,:,r705].astype(np.int16), him[:,:,r550].astype(np.int16))

#Transformed Chlorophyll Absorption Ratio Index
def tcari_cube(him, r700=127, r670=114, r550=64):
    return i.tcari_bands(him[:,:,r700].astype(np.int16), him[:,:,r670].astype(np.int16), him[:,:,r550].astype(np.int16))

#Optimised Soil-Adjusted Vegetation Index
def osavi_cube(him, r800=169, r670=114):
    return i.osavi_bands(him[:,:,r800].astype(np.int16), him[:,:,r670].astype(np.int16))

#Zarco Tejada & Miller
def ztm_cube(him, r750=185, r710=140):
    return i.ztm_bands(him[:,:,r750], him[:,:,r710])

#Improved Soil Adjusted Vegetation Index
def msavi_cube(him, r800=135, r670=122):
    return i.msavi_bands(him[:,:,r800], him[:,:,r670])

#Double peak Index
def dpi_cube(him, r688=122, r710=131, r697=126):
    return i.dpi_bands(him[:,:,r710].astype(np.int16), him[:,:,r697].astype(np.int16), him[:,:,r688].astype(np.int16)) 

#Curvature Index
def ci_cube(him, r675=116, r690=123, r683=120):
    return i.ci_bands(him[:,:,r675], him[:,:,r690], him[:,:,r683])
