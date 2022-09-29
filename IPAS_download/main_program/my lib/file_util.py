import os
import logging
import json
from win32com import client as wincom_client


def get_file_version(file_path):
    #logging.info('get file path on [%s]'.format(file_path))
    if not os.path.exists(file_path):
        raise FileNotFoundError("{!r} file not found".format(file_path))
    
    wincom_job = wincom_client.Dispatch('Scripting.FileSystemObject')
    version = wincom_job.GetFileVersion(file_path)
    #logging.info('The file version of [%s] is %s', file_path, version)
    return version.strip()

def write_json(file_path, info):
    with open(file_path, 'w') as f:
        json.dump(info, f, indent = 2)


def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data






if __name__ == "__main__":
    file_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    print(get_file_version(file_path))
    

    

    