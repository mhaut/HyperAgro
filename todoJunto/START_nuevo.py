import argparse
import logging
import cv2, signal, sys, os, shutil, traceback, glob, time
from datetime import datetime
from telegram_debugger import sendMSG
import utils


def main(args):
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    logger = get_logger(parent_folder)

    try:
        # MENSAJE INICIAL DE TELEGRAM
        msg = ""
        for i in range(6): msg += ":black_square_button:" 
        msg += "  Inicio de Captura  "
        for i in range(6): msg += ":black_square_button:"
        sendMSG(msg)

        # PATH
        parent_folder = os.path.dirname(os.path.abspath(__file__))
        saving_folder = os.path.join(parent_folder, args.pathsave)

        if not os.path.exists(saving_folder):
            os.mkdir(saving_folder)

        # LISTA DE CAMARAS A UTILIZAR
        cam_list = utils.read_cam_list(args.pathfile)

        CAPTURE_MOMENT_ISOFORMAT = "11:14:40"
        BASE_ISOFORMAT = "2022-05-26T"

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            # Esperamos hasta la siguiente hora target antes de la siguiente captura
            utils.waitTillTargetTime("21:00:00") # HORA DEL DIA A LA QUE SE REALIZA LA CAPTURA (formato 24 horas)

            # Sacamos el instante unico para toda la tanda de frames
            instant_str = datetime.now().isoformat()
            print("\n--------------------  " + instant_str + "  --------------------")

            FRAME_KIB_SIZE = 500
            if utils.full_disk(FRAME_KIB_SIZE):
                time.sleep(WAIT_TIME_ON_FULL_DISK)
                continue

            # Guardamos un frame por cada camara
            for cam_entry in cam_list:
                cam_path, cam_pos, cam_correction = cam_entry["path"], cam_entry["pos"], cam_entry["correction"]

                for i in range(20):
                    ret, frame = utils.get_image(cam_path)
                    if ret == False: continue
                    else:
                        ret, frame = data
                        break

                # Si hubo exito, guardamos e imprimimos
                img_save_path = os.path.join(saving_folder, instant_str + "___pos_" + str(cam_pos) + "___cam_" + cam_path.split("video")[-1] + ".jpg")
                cv2.imwrite(img_save_path, frame)
                print("guardado")

    except Exception as e:
        # Mensaje de error al telegram
        sendMSG("ERROR", is_error=True)
        sendMSG(traceback.format_exc(), is_error=True)
        msg = ""
        for i in range(15): msg += ":white_square_button:"
        sendMSG(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HyperGreen')
    parser.add_argument('--pathsave',    , type=str  default='saving'   , help='image directory')
    parser.add_argument('--time_fulldisk', type=int, default=3600       , help='segundos de espera entre mensajes de "disco lleno"')
    parser.add_argument('--logfile',     , type=str  default='myapp.log', help='log file')
    args = parser.parse_args()
	main(args)
