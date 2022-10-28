import configparser
import os
from copy import deepcopy

INI_path = r"D:\Qian\python\NPI\Gemini\value_config.ini"
data = {}

def read_ini(INI_path):
    Tmp_data = {}
    config = configparser.ConfigParser()
    config.read(INI_path)

    for section in config.sections():
        for k in config[section]:
            Tmp_data[k] = config[section][k]
        
        data[section] = deepcopy(Tmp_data)
        Tmp_data.clear()
    
    return data
    
    


if "__main__" == __name__:
    read_ini(INI_path)
    print(data)