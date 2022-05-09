from colored import fg

B = fg(238)
W = fg(15)
C = fg(193)
print(B, " ")

import cv2, signal, sys, os, shutil, traceback, glob, time
from datetime import datetime
from telegram_debugger import sendMSG
from img_sender import tryToSendNewPacks


try:

    # MENSAJE INICIAL DE TELEGRAM
    msg = ""
    for i in range(6): msg += ":black_square_button:" 
    msg += "  Inicio de Captura  "
    for i in range(6): msg += ":black_square_button:"

    sendMSG(msg)



    # PATH
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    saving_folder = os.path.join(parent_folder, "saving")

    if not os.path.exists(saving_folder):
        os.mkdir(saving_folder)


    # LISTA DE CAMARAS A UTILIZAR
    cam_path_list = [
        "/dev/video0",
        "/dev/video2",
        "/dev/video4",
        "/dev/video6",
        "/dev/video8",
        "/dev/video10"
    ]


    # CONSTANTES
    FRAME_WIDTH = 1920
    FRAME_HEIGHT = 1080
    ROTATE_IMG = cv2.ROTATE_90_COUNTERCLOCKWISE # Usar None para no rotar o cv2.ROTATE_90_CLOCKWISE para rotarla (cv2.ROTATE_90_COUNTERCLOCKWISE)

    EXPO_NUM_FRAMES = 10
    FRAME_KIB_SIZE = 500
    MIN_FREE_SPACE = 4 # En GiB
    TELEGRAM_INFO_PERIOD = 100 # Vueltas de bucle para enviar info al telegram
    SEND_FTP_PERIOD = 1 # Cada cuantos packs se envian las imagenes al server ftp
    WAIT_TIME_ON_FULL_DISK = 1 # SEGUNSDOS DE ESPERA ENTRE MENSAJES DE "DISCO LLENO"




    ######################################################################
    ######################################################################
    ######################################################################
    """                          SIGINT Handler                        """
    ######################################################################
    ######################################################################
    ######################################################################


    def signal_handler(sig, frame):
        """
        Handler de SIGINT (Ctrl + C) para cerrar los flujos 
        de las camaras al cerrar el programa.
        """
        print(fg(11) + 'Ctrl+C detectado. Liberando flujos y cerrando programa...' + W)

        try:
            # Liberamos las camaras
            print(fg(11) + 'Liberando flujos' + B)
            cam.release()
            cv2.destroyAllWindows()
        except:
            pass

        sendMSG("Ctrl+C detectado. Saliendo del programa")
        msg = ""
        for i in range(15): msg += ":white_square_button:"
        sendMSG(msg)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)








    ######################################################################
    ######################################################################
    ######################################################################
    """                               MAIN                             """
    ######################################################################
    ######################################################################
    ######################################################################

    # cada X iteraciones se envia info al telegram
    t_info_counter = 0
    t_send_counter = 0
    

    while True:


        # Sacamos el instante unico para toda la tanda de frames
        instant_str = datetime.now().isoformat()
        print(C + "\n--------------------  " + W + instant_str + C + "  --------------------")
        total, used, free = shutil.disk_usage("/")

        frames_left = (free // (2**10)) // FRAME_KIB_SIZE # un frame aprox 280 KiB a 720p o 500KiB a 1080p
        img_num = len(glob.glob(os.path.join(saving_folder, "*.jpg")))
        print(fg(202) + "Espacio libre en disco: " + fg(14) + str(free // (2**20)) + fg(202) + " MiB  (" + fg(14) + str(frames_left) + fg(202) + " frames)" + B)
        print(fg(202) + "Imagenes actuales: " + fg(14)  + str(img_num) + fg(202) + " (" + fg(14) + str(img_num // len(cam_path_list)) + fg(202) + " packs)" + B)

        # Info para telegram
        if t_info_counter % TELEGRAM_INFO_PERIOD == 0:
            sendMSG("Espacio libre en disco: "+ str(free // (2**20)) + " MiB  (" + str(frames_left) + " frames)", dont_print=True)
            sendMSG("Imagenes actuales: " + str(img_num) + " (" + str(img_num // len(cam_path_list)) + " packs)", dont_print=True)
            

        # Comprobacion de seguridad de espacio libre
        if (free // (2**30)) < MIN_FREE_SPACE:
            print(fg(9) + "[!] QUEDAN MENOS DE " + W + str(MIN_FREE_SPACE) + fg(9) + " GiB LIBRES [!]" + W)
            sendMSG("[!] QUEDAN MENOS DE " + str(MIN_FREE_SPACE) + " GiB LIBRES [!]", is_warning=True, dont_print=True)
            time.sleep(WAIT_TIME_ON_FULL_DISK)
            continue

        # Guardamos un frame por cada camara
        for cam_path in cam_path_list:
            # Conectamos con la camara
            cam = cv2.VideoCapture(cam_path)

            # Si la camara no es valida, descartamos
            if not (cam.isOpened()):
                print(W + "Entrada de video " + str(cam_path) + fg(9) + " no valida." + B)
                sendMSG("Entrada de video " + str(cam_path) + " no valida.", is_warning=True, dont_print=True)
                continue
            print(W + "Entrada de video " + str(cam_path) + fg(10) + " valida." + B)
            
            # Configuramos las camaras validas
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

            # Sacamos frames para que la exposicion automatica se estabilice
            for i in range(EXPO_NUM_FRAMES):
                ret, frame = cam.read()

            # Sacamos el frame definitivo
            ret, frame = cam.read()

            # Rotamos si es necesario
            if ROTATE_IMG != None:
                frame = cv2.rotate(frame, ROTATE_IMG)


            # Guardamos el frame
            if ret == True:
                cam_number = cam_path.split("video")[-1]
                img_save_path = os.path.join(saving_folder, instant_str + "___cam_" + cam_number + ".jpg")
                cv2.imwrite(img_save_path, frame)
            else:
                print(fg(9) + "Bad Frame" + W + cam_path)
                sendMSG("Bad Frame" + cam_path, is_warning=True, dont_print=True)

            
            # Liberamos el flujo
            cam.release()
        

        # Cada X packs, intentamos enviar las imagenes al servidor
#        if t_send_counter % SEND_FTP_PERIOD == 0:
#            tryToSendNewPacks()
        


        # Reseteamos
        t_info_counter += 1
        t_send_counter += 1

except Exception as e:
    # Mensaje de error al telegram
    sendMSG("ERROR", is_error=True)
    sendMSG(traceback.format_exc(), is_error=True)

    msg = ""
    for i in range(15): msg += ":white_square_button:"
    sendMSG(msg)
