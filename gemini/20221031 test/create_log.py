import os
import logging
import logging.handlers


def create_logger(dir_path, filename):
    filename = filename + '.log'
    filepath = os.path.join(dir_path, filename)
    
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG) 

    fileHandler = logging.FileHandler(filepath, 'w', 'utf-8')
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.WARNING) 
    
    formatter = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)  #將log印到螢幕上
    #logger.addHandler(consoleHandler)  #將logger印到終端機上

    return logger




if __name__ == "__main__":
    file_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    print(get_file_version(file_path))
    

    

    