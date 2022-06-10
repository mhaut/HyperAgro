#Logica de ejecucion
# 1º Se espera a que llegue el momento de la captura
# 2º Se realiza la captura de las imagenes rgb
# 3º Se realiza la captura de la imagen hyper
# 4º Paso 1º

import os
import time
import re

def main (args) 
    # Se obtienen las rutas de las carpetas relevantes 
    parent_folder       = os.path.dirname(os.path.abspath(__file__))
    shared_folder       = os.path.dirname(parent_folder, args.shared_folder)
    rgb_saving_folder   = os.path.dirname(shared_folder, args.rgb_folder)
    hyper_saving_folder = os.path.dirname(shared_folder, args.pathsaveHyper)
    # Se crean los directorios si no existen
    [os.mkdir(folder) for folder in [shared_folder, rgb_saving_folder, hyper_saving_folder] if not os.path.exists(folder)]
    #Se obtiene el logger para escribir el output
    logger = get_logger(parent_folder)
    # Se obtiene la lista de las camaras RGB
    cam_list = utils.read_cam_list(lab=False)
    # Se definen ventanas y marcas de tiempo para su posterior uso
    capture_instant_isoformat = "14:00:00"
    wait_time_full_disk = 3600           
    #Se sobrescribe la senal cntrl+c
    signal.signal(signal.SIGINT, utils.signal_handler)
    while True:
        # Esperamos hasta la siguiente hora target antes de la siguiente captura
        logger.info("Proceso dormido")
        utils.waitTillTargetTime(capture_instant_isoformat) 
        #Se obtiene el instante en el que se van a tomar las imagenes RGB
        capture_timestamp = datetime.now().isoformat()
        logger.info(f"Instante de captura RGB->\t\t{capture_timestamp}")
        #Se registra el uso de disco
        FRAME_KIB_SIZE = 500
        if utils.full_disk(FRAME_KIB_SIZE, logger):
            time.sleep(wait_time_full_disk)
            continue
        #Se realiza la captura RGB para cada una de las camaras, hasta 20 intentos por cada una
        try:
            for cam_entry in cam_list:
                cam_path, cam_pos, cam_correction = cam_entry["path"], cam_entry["pos"], cam_entry["correction"]
                for i in range(20):
                    ret, frame = utils.get_image_rgb(cam_path)
                    if ret == False: continue
                    else:
                        ret, frame = data
                        break
                # Si (ret == True) -> se guarda la imagen, si no -> se guarda un frame negro
                img_name = instante_captura + "___pos_" + str(cam_pos) + "___cam_" + cam_path.split("video")[-1] + ".jpg"
                img_save_path = os.path.join(rgb_saving_folder, img_name)
                cv2.imwrite(img_save_path, frame)
                if ret: logger.info("Se ha guardado la imagen", img_name)
                else:   logger.info("No se ha podido guardar la imagen", img_name, "se guarda un frame negro")
        except Exception as e:
            logger.info("Ha habido un error durante la captura RGB")
            logger.info(e.message)
        
        #Se obtiene el instante en el que se van a tomar las imagenes Hyper
        try:
            capture_timestamp = datetime.now().isoformat()
            logger.info(f"Instante de captura Hyper->\t\t{capture_timestamp}")
            
            sensor = nano.Nano(verbose=args.verbosity)
            sensor.connect()
            sensor.configure(exposure=args.exposureTime, framePeriod=args.framePeriod)
            source_folder = sensor.capture(prefix=args.prefix, maxCubes=args.maxCubes, maxFramesPerCube=args.maxFramesPerCube)["folder"]
           
            while sensor.isCapturing(): pass
            
            logger.info("La captura de la imagen espectral ha terminado")

            get_image_hyper(os.path.abspath(join(parent_folder, args.credentials)),source_folder, hyper_saving_folder, capture_timestamp, logger)
        except Exception as e:
            logger.info("Ha habido un error durante la captura Hyper")
            logger.info(e.message)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HyperGreen')
    #Directorio compartido
    parser.add_argument('--sharedFolder',      type=str,  default='saving',   help='Directorio compartido')
    #Parametros de la captura RGB
    parser.add_argument('--pathsaveRGB',      type=str,  default='rgb',       help='Directorio donde se guardan las imagenes RGB')
    parser.add_argument('--time_fulldisk',    type=int,  default=3600,        help='segundos de espera entre mensajes de "disco lleno"')
    parser.add_argument('--logfile',          type=str,  default='myapp.log', help='log file')
    #Parametros de la captura Hiper
    parser.add_argument('--pathsaveHyper',    type=str,  default='hyper',     help='Directorio donde se guardan las imagenes Hyper')
    parser.add_argument('--credentials',    type=str,  default='credentialsHyper.json',     help='Fichero donde se guardan las credenciales Hyper')
    parser.add_argument('--verbosity',        type=bool, default=False,       help='ON/OFF del modo verbose de logging de la camara hiper')
    parser.add_argument('--exposureTime',     type=int,  default=20,          help='Tiempo de exposicion de la camara Hiper')
    parser.add_argument('--framePeriod',      type=int,  default=21,          help='Periodo de captura de lineas')
    parser.add_argument('--prefix',           type=str,  default='',          help='Prefijo de la carpeta de las capturas')
    parser.add_argument('--maxCubes',         type=int,  default=1,           help='Numero maximo de cubos por captura')
    parser.add_argument('--maxFramesPerCube', type=int,  default=2000,        help='Numero de frames (lineas) por cubo')
    args = parser.parse_args()
	main(args)
