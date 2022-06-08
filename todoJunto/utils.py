from datetime import datetime
import time 



BASE_DATETIME_DATE   = "2000-01-01T" # NO CAMBIAR



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


def signal_handler(sig, frame):
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
    sendMSG("Ctrl+C detectado. Saliendo del programa")
    msg = ""
    for i in range(15): msg += ":white_square_button:"
    sendMSG(msg)
    sys.exit(0)


def read_cam_list(pathfile=None):
    return [
            {"path": "/dev/video0",  "pos": 0, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video10", "pos": 1, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video8",  "pos": 2, "correction": cv2.ROTATE_90_COUNTERCLOCKWISE},
            {"path": "/dev/video12", "pos": 3, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video6",  "pos": 4, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video4",  "pos": 5, "correction": cv2.ROTATE_90_CLOCKWISE},
            {"path": "/dev/video2",  "pos": 6, "correction": cv2.ROTATE_90_CLOCKWISE}
        ]


def full_disk(frame_KB_size):
    MIN_FREE_SPACE = 4
    total, used, free = shutil.disk_usage("/")

    frames_left = (free // (2**10)) // frame_KB_size # un frame aprox 280 KiB a 720p o 500KiB a 1080p
    img_num = len(glob.glob(os.path.join(saving_folder, "*.jpg")))
    print("Espacio libre en disco:", free // (2**20), "MiB (" + str(frames_left), "frames)")
    print("Imagenes actuales:", img_num, "(" + str(img_num // len(cam_list)), "packs)")

    # Info para telegram
    sendMSG("Espacio libre en disco:", free // (2**20), "MiB  (" + str(frames_left), "frames)", dont_print=True)
    sendMSG("Imagenes actuales:", img_num, "(" + str(img_num // len(cam_list)), "packs)", dont_print=True)

    # Comprobacion de seguridad de espacio libre
    if (free // (2**30)) <= MIN_FREE_SPACE:
        string = "[!] QUEDAN MENOS DE " + str(MIN_FREE_SPACE) + " GB LIBRES [!]"
        sendMSG(string, is_warning=True, dont_print=True)
        return False
    return True


def get_image(cam_path):
    # CONSTANTES
    FRAME_WIDTH = 1920
    FRAME_HEIGHT = 1080
    EXPO_NUM_FRAMES = 10
    # Conectamos con la camara
    cam = cv2.VideoCapture(cam_path)

    # Si la camara no es valida, descartamos y avisamos
    if not (cam.isOpened()):
        string = "Entrada de video " + str(cam_path) + " no valida."
        sendMSG(string, is_warning=True, dont_print=True)
        frame = np.zeros((FRAME_WIDTH,FRAME_HEIGHT,3), dtype=np.uint8)
        return False, frame
    print("Entrada de video " + str(cam_path) + " valida.", end=" ")   
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
    # Liberamos el flujo
    cam.release()
    if ret == False: frame = np.zeros((FRAME_WIDTH,FRAME_HEIGHT,3), dtype=np.uint8)
    return ret, frame
