import logging
import logging.handlers

def create_logger(filepath, filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG) 

    fileHandler = logging.FileHandler(filepath, 'w+', 'utf-8')
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.WARNING) 
    
    formatter = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)  #將log印到螢幕上

    return logger