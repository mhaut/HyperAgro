from colored import fg

B = fg(238)
W = fg(15)
C = fg(193)
print(B, " ")

import cv2, signal, sys, os, shutil, traceback, glob, time
from datetime import datetime
from telegram_debugger import sendMSG


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
    cam_list = [
        {"path" : "/dev/video0",  "pos" : 0, "correction" : cv2.ROTATE_90_COUNTERCLOCKWISE},
        {"path" : "/dev/video10", "pos" : 1, "correction" : cv2.ROTATE_90_COUNTERCLOCKWISE},
        {"path" : "/dev/video8",  "pos" : 2, "correction" : cv2.ROTATE_90_COUNTERCLOCKWISE},
        {"path" : "/dev/video12", "pos" : 3, "correction" : cv2.ROTATE_90_CLOCKWISE},
        {"path" : "/dev/video6",  "pos" : 4, "correction" : cv2.ROTATE_90_CLOCKWISE},
        {"path" : "/dev/video4",  "pos" : 5, "correction" : cv2.ROTATE_90_CLOCKWISE},
        {"path" : "/dev/video2",  "pos" : 6, "correction" : cv2.ROTATE_90_CLOCKWISE}
    ]


    # CONSTANTES
    FRAME_WIDTH = 1920
    FRAME_HEIGHT = 1080

    EXPO_NUM_FRAMES = 10
    FRAME_KIB_SIZE = 500
    MIN_FREE_SPACE = 4 # En GiB
    WAIT_TIME_ON_FULL_DISK = 3600 # SEGUNDOS DE ESPERA ENTRE MENSAJES DE "DISCO LLENO"

    CAPTURE_MOMENT_ISOFORMAT = "11:14:40"
    BASE_ISOFORMAT = "2022-05-26T"

    BASE_DATETIME_DATE   = "2000-01-01T" # NO CAMBIAR
    TARGER_DATETIME_TIME = "21:00:00" # HORA DEL DIA A LA QUE SE REALIZA LA CAPTURA (formato 24 horas)









    def getSecondsToNextTarget():
        """
        Funcion que devuelve los segundos que faltan 
        para llegar a la hora target del dia. Si se ha pasado 
        la hora target, indica los segundos hasta la siguiente hora target.
        """
        current_time_iso = datetime.now().time().isoformat()
        current_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + current_time_iso)

        target_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + TARGER_DATETIME_TIME)

        delta_time = target_compare_datetime - current_compare_datetime

        return delta_time.seconds
    



    def waitTillTargetTime():
        """
        Funcion que duerme el proceso hasta que llega la hora target.
        """

        STT = getSecondsToNextTarget()
        # Esperamos la mitad del tiempo hasta que queden menos de X segundos
        while STT > 60:
            sendMSG("Durmiendo " + str(STT//2) + " segundos", dont_print=True)
            time.sleep(STT//2)
            STT = getSecondsToNextTarget()
        
        # Dormimos lo que queda
        sendMSG("Durmiendo ultimos" + str(STT) + " segundos", dont_print=True)
        time.sleep(STT)








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

    

    while True:

        # Esperamos hasta la siguiente hora target antes de la siguiente captura
        #waitTillTargetTime()


        # Sacamos el instante unico para toda la tanda de frames
        instant_str = datetime.now().isoformat()
        print(C + "\n--------------------  " + W + instant_str + C + "  --------------------")
        total, used, free = shutil.disk_usage("/")

        frames_left = (free // (2**10)) // FRAME_KIB_SIZE # un frame aprox 280 KiB a 720p o 500KiB a 1080p
        img_num = len(glob.glob(os.path.join(saving_folder, "*.jpg")))
        print(fg(202) + "Espacio libre en disco: " + fg(14) + str(free // (2**20)) + fg(202) + " MiB  (" + fg(14) + str(frames_left) + fg(202) + " frames)" + B)
        print(fg(202) + "Imagenes actuales: " + fg(14)  + str(img_num) + fg(202) + " (" + fg(14) + str(img_num // len(cam_list)) + fg(202) + " packs)" + B)

        # Info para telegram
        sendMSG("Espacio libre en disco: "+ str(free // (2**20)) + " MiB  (" + str(frames_left) + " frames)", dont_print=True)
        sendMSG("Imagenes actuales: " + str(img_num) + " (" + str(img_num // len(cam_list)) + " packs)", dont_print=True)
        

        # Comprobacion de seguridad de espacio libre
        if (free // (2**30)) < MIN_FREE_SPACE:
            print(fg(9) + "[!] QUEDAN MENOS DE " + W + str(MIN_FREE_SPACE) + fg(9) + " GiB LIBRES [!]" + W)
            sendMSG("[!] QUEDAN MENOS DE " + str(MIN_FREE_SPACE) + " GiB LIBRES [!]", is_warning=True, dont_print=True)
            time.sleep(WAIT_TIME_ON_FULL_DISK)
            continue

        # Guardamos un frame por cada camara
        for cam_entry in cam_list:

            cam_path = cam_entry["path"]
            cam_pos = cam_entry["pos"]
            cam_correction = cam_entry["correction"]



            # Conectamos con la camara
            cam = cv2.VideoCapture(cam_path)

            # Si la camara no es valida, descartamos y avisamos
            if not (cam.isOpened()):
                print(W + "Entrada de video " + str(cam_path) + fg(9) + " no valida." + B)
                sendMSG("Entrada de video " + str(cam_path) + " no valida.", is_warning=True, dont_print=True)
                continue
            print(W + "Entrada de video " + str(cam_path) + fg(10) + " valida." + B, end=" ")
            
            # Configuramos las camaras validas
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

            # Sacamos frames para que la exposicion automatica se estabilice
            for i in range(EXPO_NUM_FRAMES):
                ret, frame = cam.read()

            # Sacamos el frame definitivo
            ret, frame = cam.read()

            # Ralizamos la correccion pertinente a la imagen de la camara X
            frame = cv2.rotate(frame, cam_correction)


            # Guardamos el frame
            frame_succes = False

            while frame_succes == False:

                if ret == True:
                    # Si hubo exito, guardamos e imprimimos
                    cam_number = cam_path.split("video")[-1]
                    img_save_path = os.path.join(saving_folder, instant_str + "___pos_" + str(cam_pos) + "___cam_" + cam_number + ".jpg")
                    cv2.imwrite(img_save_path, frame)

                    img_save_path = os.path.join(saving_folder, instant_str + "___pos_" + str(cam_pos) + "___cam_" + cam_number + "EEE.jpg")
                    cv2.imwrite(img_save_path, cv2.equalizeHist(frame))
                    print(fg(10) + "guardado" + B)
                    frame_succes = True
                else:
                    # Si no hubo exito, avisamos y reiniciamos
                    print(fg(9) + "Bad Frame" + W + cam_path)
                    sendMSG("Bad Frame" + cam_path, is_warning=True, dont_print=True)

                    # Montamos de nuevo la conexión con el flujo y la extraccion de la imagen
                    cam = cv2.VideoCapture(cam_path)
                    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                    for i in range(EXPO_NUM_FRAMES):
                        ret, frame = cam.read()
                    ret, frame = cam.read()
                    frame = cv2.rotate(frame, cam_correction)
            

            # Liberamos el flujo
            cam.release()

        
        

        


except Exception as e:
    # Mensaje de error al telegram
    sendMSG("ERROR", is_error=True)
    sendMSG(traceback.format_exc(), is_error=True)

    msg = ""
    for i in range(15): msg += ":white_square_button:"
    sendMSG(msg)
