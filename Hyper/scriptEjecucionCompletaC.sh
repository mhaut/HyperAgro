instrucciones="Formatos aceptados: \n\t./scriptVisualizacionC.sh <NombreficheroDestino> \n\t./scriptVisualizacionC.sh <NombreficheroDestino> <ObjectID_ImagenEspectral>\n"
ejemplo="Ejemplos de uso: \n\t./scriptVisualizacionC.sh HIM.bin \n\t./scriptVisualizacionC.sh HIM.bin 6245dd668a1e25a2675a7390\n"

if [ $# -eq 0 ]; then
    printf "$instrucciones"
    printf "$ejemplo"
    exit
fi   

printf "Se va a ejecutar la captura de una imagen espectral\n"

/usr/bin/python3.8 nanoScript.py 

printf "La imagen espectral se almacenara en el siguiente fichero -> $1\n"
sudo ../Indices/extraccion $1
sudo chmod +rwx "./$1"
printf "La imagen esta lista para ser manipulada, se proporciona una previsualizacion\n"

/usr/bin/python3.8 ../Indices/Previsualizacion.py $1
