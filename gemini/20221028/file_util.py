import os
import logging
import json
from win32com import client as wincom_client
import logging
import logging.handlers


def get_file_version(file_path):
    logging.info('get file path on [%s]'.format(file_path))
    if not os.path.exists(file_path):
        raise FileNotFoundError("{!r} file not found".format(file_path))
    
    wincom_job = wincom_client.Dispatch('Scripting.FileSystemObject')
    version = wincom_job.GetFileVersion(file_path)
    logging.info('The file version of [%s] is %s', file_path, version)
    return version.strip()

def write_json(file_path, info):
    with open(file_path, 'w') as f:
        json.dump(info, f, indent = 2)


def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


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
    

    

    