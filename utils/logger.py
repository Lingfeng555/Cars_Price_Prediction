import logging
import os

class Logger:
    """
    A utility class for setting up logging to both a file and the console.

    Purpose:
        - Simplifies logging configuration by handling file and console logging in one class.
        - Automatically creates the log directory if it doesn't exist.

    Parameters:
        name (str): The name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (default: logging.INFO).

    Methods:
        __init__: 
            - Initializes the logger with the specified name, log file, and logging level.
            - Configures separate handlers for writing logs to a file and the console.
        get_logger:
            - Returns the configured logger instance for use in other parts of the application.

    Notes:
        - The log messages are formatted with timestamps, logger names, log levels, and messages.
        - Logs are both saved to the specified file and displayed in the console.

    Example Usage:
        >>> logger = Logger("MyApp", "logs/myapp.log").get_logger()
        >>> logger.info("Application started.")
    """
    
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
