import logging
import os

class Logger:
    def __init__(self, name, log_file, level=logging.INFO):
        # Crea el directorio para el archivo de log si no existe
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Crea un logger con el nombre proporcionado
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Crea un formateador de mensajes de log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Crea un manejador de log que escribe en un archivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Crea un manejador de log que escribe en la consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
