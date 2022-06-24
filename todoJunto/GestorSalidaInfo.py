import logging
from multiprocessing import Queue

class GestorSalidaInfo:
    
    def __init__(self):
        self.logger = self.prepararLogger()

    def prepararLogger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

        stdout_handler.setFormatter(formatter)

        logger.addHandler(stdout_handler)
        return logger

    def printDEBUG(self, contexto, mensaje):       
        self.logger.debug("{: <25} | {}".format(contexto, mensaje))

    def printINFO(self, contexto, mensaje):
        self.logger.info("{: <25} | {}".format(contexto, mensaje))

    def printWARNING(self, contexto, mensaje):
        self.logger.warning("{: <25} | {}".format(contexto, mensaje))

    def printERROR(self, contexto,mensaje):
        self.logger.error("{: <25} | {}".format(contexto, mensaje))

