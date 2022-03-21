import ftplib, os, glob, traceback
from datetime import datetime
from telegram_debugger import sendMSG
from emoji import emojize




# PATH
parent_folder = os.path.dirname(os.path.abspath(__file__))
saving_folder = os.path.join(parent_folder, "saving")

time_ref_path = os.path.join(saving_folder, "TEMP_REF")
ftp_credentials_path = os.path.join(parent_folder, "ftp_credentials")


# Constantes
SEND_ATTEMPS = 2
MIN_TIME_REF_ISOFORMAT = "2022-03-07T13:57:43.532813" # "2000-01-01T00:00:00.000000"


def tryToSendNewPacks():
    """
    Realiza SEND_ATTEMPS intentos de envio de las nuevas imagenes 
    que encuentre.

    Se consideran imagenes nuevas aquellas que tengan una marca 
    de tiempo mas reciente que la guardada en el archivo de referencia.

    Si no hay archivo de referencia, lo crea con una fecha muy antigua.
    """

    

    # Cargamos el archivo con la marca de tiempo
    if os.path.isfile(time_ref_path):
        # Si el archivo existe lo cargamos
        time_file = open(time_ref_path, "r")
        time_ref = datetime.fromisoformat(time_file.read())
    else:
        # Si el archivo no existe, cogemos la marca de tiempo minima
        time_ref = datetime.fromisoformat(MIN_TIME_REF_ISOFORMAT)
    

    # Obtenemos los path de todas las imagenes almacenadas
    img_path_list = glob.glob(os.path.join(saving_folder, "*.jpg"))

    print(len(img_path_list), " imagenes en la carpeta savings.")

    # Quitamos las imagenes anteriores a la marca de tiempo
    new_img_list = []
    old_img_list = []
    newest_datetime = time_ref
    i = 0
    for img_path in img_path_list:
        # Obtenemos el datetime de la imagen
        img_iso = os.path.basename(img_path).split("___")[0]
        img_datetime = datetime.fromisoformat(img_iso)

        # Clasificamos las imagenes por antiguas y nuevas respcto dela marca de tiempo
        if time_ref >= img_datetime:
            old_img_list.append(img_path)
        else:
            new_img_list.append(img_path)

            # Actualizamos para quedarnos con la marca de tiempo mas moderna
            if img_datetime > newest_datetime:
                newest_datetime = img_datetime
        

    print(len(new_img_list), " imagenes nuevas.")
    print(len(old_img_list), " imagenes antiguas.")
    print("Marca de tiempo mas moderna: " + newest_datetime.isoformat())

    
    # Enviamos las imagenes nuevas

    # Leemos de archivo las credenciales
    try:
        ftp_credentials_file = open(ftp_credentials_path, "r")
        ftp_credentials_list = ftp_credentials_file.read().split("\n")
    except Exception as e:
        raise e


    try:
        # Iniciamos sesion
        session = ftplib.FTP(ftp_credentials_list[0], ftp_credentials_list[1], ftp_credentials_list[2])

        # Cambiamos la carpeta remota destino
        session.cwd(ftp_credentials_list[3])

        # Enviamos las imagenes nuevas
        for img_path in new_img_list:
            # Abrimos la imagen
            img_file = open(img_path,'rb')
            # Enviamos la imagen
            session.storbinary("STOR " + os.path.basename(img_path), img_file)
            # Cerramos la imagen
            img_file.close()
        
        #msg = emojize("Tanda de " + str(len(new_img_list)) + " imagenes enviadas :check_mark_button:")
        #sendMSG(msg)
        
        # Cerramos la sesion FTP
        session.quit()
    except:
        # Avisamos del error y terminamos la funcion para que no se registre 
        # la marca de tiempo y se pueda volver a intentar mas tarde
        msg = emojize("Error al enviar las imagenes :red_exclamation_mark:")
        sendMSG(msg)
        sendMSG("Este es el error:\n\n" + traceback.format_exc())
        return


    # Actualizamos la marca de tiempo en archivo
    time_file = open(time_ref_path, "w")
    time_file.write(newest_datetime.isoformat())







