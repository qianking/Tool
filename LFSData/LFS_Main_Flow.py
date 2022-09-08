import os 
import sys
import re
from glob import glob

path = r'C:\Users\andy_chien\Downloads\弱層資料整理_1\弱層資料整理\INPUT'
num = None

find_file_name = ('INPUT_RCD', 'INPUT_REBAR', 'INPUT_WALLDA', f'{num}INPUT_WALLDA', f'{num}INPUT', f'{num}SHEAR')

def send_to_ui(txt):
    pass

def main_flow(path):
    file_list = glob(f"{path}\*.txt")

    file_name_list = get_number_from_file(file_list)
    if not num:
        send_to_ui(f'找不到案號檔案')
        return 0

    loose_file = check_file_exist(file_name_list)
    if loose_file:
        send_to_ui(f'找不到檔案{loose_file}')
        return 0
    
    print('ok')
    

    
    
    







def check_file_exist(file_name_list):
    loose_file = list()
    for file_name in file_name_list:
        if file_name not in find_file_name:
            loose_file.append(file_name)
    print(loose_file)
    if len(loose_file):
        return loose_file
    return 0

def get_number_from_file(file_list):
    global num
    file_name_list = [file.split('\\')[-1].split('.')[0] for file in file_list]
    pattern = re.compile(r"(^[A-Z]\d\d\d)", re.I)
    for file_name in file_name_list:
        find =pattern.findall(file_name)
        if len(find):
            print(find)
            num = find[0]
            break
    if num:  
        return file_name_list
    return 0

if "__main__" == __name__:
    main_flow(path)