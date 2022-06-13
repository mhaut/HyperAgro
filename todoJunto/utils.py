import cv2
from datetime import datetime
import logging
import shutil, glob
import os
import sys
import time 
from telegram_debugger import sendMSG
import numpy as np
import json

BASE_DATETIME_DATE   = "2000-01-01T" # NO CAMBIAR

def get_logger(parent_folder, log_file save_logfile=False):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    if save_logfile:
        file_handler = logging.FileHandler(os.path.join(parent_folder, args.logfile))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    return logger


def getSecondsToNextTarget(target_datetime_time):
    """
    Funcion que devuelve los segundos que faltan 
    para llegar a la hora target del dia. Si se ha pasado 
    la hora target, indica los segundos hasta la siguiente hora target.
    """
    current_time_iso = datetime.now().time().isoformat()
    current_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + current_time_iso)
    target_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + target_datetime_time)
    delta_time = target_compare_datetime - current_compare_datetime
    return delta_time.seconds


def waitTillTargetTime(target_datetime_time):
    """
    Funcion que duerme el proceso hasta que llega la hora target.
    """
    STT = getSecondsToNextTarget(target_datetime_time)
    # Dormimos lo que queda
    time.sleep(STT)




# Lista con los directorios en los que se encuentran montadas las camaras
def read_cam_list(pathfile=None, lab=True):
    if lab == True:
        return [
            {"path": "/dev/video0",  "pos": 0, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            #{"path": "/dev/video2", "pos": 2, "correction": cv2.ROTATE_90_CLOCKWISE}
            ]
    
    else: # mofrague
        return [
            {"path": "/dev/video0",  "pos": 0, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video10", "pos": 1, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video8",  "pos": 2, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video12", "pos": 3, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video6",  "pos": 4, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video4",  "pos": 5, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video2",  "pos": 6, "correction": cv2.ROTATE_90_CLOCKWISE}
            ]

# 
def full_disk(frame_KB_size, saving_folder, logger):
    MIN_FREE_SPACE = 4
    total, used, free = shutil.disk_usage("/")

    frames_left = (free // (2**10)) // frame_KB_size # un frame aprox 280 KiB a 720p o 500KiB a 1080p
    img_num = len(glob.glob(os.path.join(saving_folder, "*.jpg")))
    logger.info("Espacio libre en disco: " + str(free // (2**20)) + " MiB (" + str(frames_left) + " frames)")
    # Comprobacion de seguridad de espacio libre
    if (free // (2**30)) <= MIN_FREE_SPACE:
        logger.info("[!] QUEDAN MENOS DE " + str(MIN_FREE_SPACE) + " GB LIBRES [!]")
        return True
    return False


def get_image_rgb(cam_path, cam_correction, logger):
    logger.info(cam_path)
    # CONSTANTES
    FRAME_WIDTH = 1920
    FRAME_HEIGHT = 1080
    EXPO_NUM_FRAMES = 40
    # Conectamos con la camara
    cam = cv2.VideoCapture(cam_path)
    # Se reescribe la senal cntrl + c

    def signal_handler(cam):
        """
        Handler de SIGINT (Ctrl + C) para cerrar los flujos 
        de las camaras al cerrar el programa.
        """
        print('Ctrl+C detectado. Liberando flujos y cerrando programa...')
        try:
            # Liberamos las camaras
            print('Liberando flujos')
            cam.release()
            cv2.destroyAllWindows()
        except:
            pass
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Si la camara no es valida, descartamos y avisamos
    if not (cam.isOpened()):
        string = "Entrada de video " + str(cam_path) + " no valida."
        sendMSG(string, is_warning=True, dont_print=True)
        frame = np.zeros((FRAME_WIDTH,FRAME_HEIGHT,3), dtype=np.uint8)
        return False, frame
    logger.info("Entrada de video " + str(cam_path) + " valida.", end=" ")   
    # Configuramos las camaras validas
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    # Sacamos frames para que la exposicion automatica se estabilice
    for i in range(EXPO_NUM_FRAMES):
        ret, frame = cam.read()
    # Sacamos el frame definitivo
    ret, frame = cam.read()
    # Realizamos la correccion pertinente a la imagen de la camara X
    frame = cv2.rotate(frame, cam_correction)
    # Liberamos el flujo
    cam.release()
    # Se restablece la senal cntrl + c
    signal.signal(signal.SIGINT, sys.exit(0))
    if ret == False: frame = np.zeros((FRAME_WIDTH,FRAME_HEIGHT,3), dtype=np.uint8)
    return ret, frame


def get_image_hyper(credentials_path,source_folder, dest_folder, capture_timestamp, logger)
    try:
        credentials_file = open(credentials_path, "rb")
        credentials = json.load(credentials_file)
        credentials_file.close()
        ftpConn = ftp.FTP(credentials["dirIP"])
        ftpConn.login(credentials["user"], credentials["password"])
        for f in ftpConn.nlst(source_folder):
            if 'raw' in f:
                dest_filepath = os.path.abspath(join(dest_folder), 'HIM__' + capture_timestamp + ".bin")
                if f.endswith(".hdr") :
                    dest_filepath = os.path.abspath(join(dest_folder), 'HIM__' + capture_timestamp + ".hdr")
                with open(dest_filepath, 'wb') as dest_file:
                    ftpConn.retrbinary("RETR " + source_folder + "/" + f, dest_file.write)

            ftpConn.delete(source_folder + "/" + f) #Se borra el fichero leido de la camara            
        ftpConn.rmd(self.args[1]) #Se borra el directorio vaciado de la camara
        ftpConn.quit() #Se cierra la conexion
    except:
        logger.info("Ha ocurrido un error en la descarga de los ficheros") 

