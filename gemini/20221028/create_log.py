import os
import logging
import logging.handlers


def create_logger(dir_path, filename):
    filename = filename + '.log'
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    consoleHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler(filepath, 'w', 'utf-8')

    formatter = logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    
    fileHandler.setLevel(logging.DEBUG)
    consoleHandler.setLevel(logging.DEBUG) 
     
    logger = logging.getLogger(filename)
    
    logger.setLevel(logging.DEBUG) 
    logger.addHandler(fileHandler)
    #logger.addHandler(consoleHandler)  #將logger印到終端機上

    return logger




if __name__ == "__main__":
    file_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    print(get_file_version(file_path))
    

    

    