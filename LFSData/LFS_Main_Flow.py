import os 
import sys
import traceback
import re
import shutil
from glob import glob
import REBAR
import RCD
import WALLDA
import INDATA

input_path = r'C:\Users\andy_chien\Downloads\弱層資料整理_1\弱層資料整理\INPUT'
output_path = r'C:\Users\andy_chien\Downloads\弱層資料整理_1\弱層資料整理\OUTPUT_TEST'
FC = {1:490, 8:420, 17:350, 23:280}
HNDL = {'1F': 0.8, '3F': 0.9, '15F': 0.8}

ui_signal = None

def send_to_ui_data_send(dic):
    ui_signal.data_send.emit(dic)

def send_to_ui_status(txt):
    ui_signal.status.emit(txt)

def data_from_ui(data, signals):
    global ui_signal
    global FC
    global HNDL
    
    ui_signal = signals
    FC = data['FC'] 
    FC = dict(sorted(FC.items()))
    tmp = data['HNDL'] 
    tmp = dict(sorted(tmp.items()))
    for floor, num in tmp.items():
        floor = f"{floor}F"
        HNDL[floor] = num
    print(HNDL)
    return data['input_path']


def debug(func):
    def warpper(*args, **wargs):
        try:
            func(*args, **wargs)
        except Exception as ex:
            error_class = ex.__class__.__name__ #取得錯誤類型
            detail = ex.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2]#取得發生的函數名稱
            errMsg = f"{[error_class]}\n\"{fileName}\", line {lineNum}, in {funcName}\n{detail}"
            print(errMsg)
            send_to_ui_status(f'Error: {errMsg}')
    return warpper

@debug   
def main_flow(data, signals=None):
    input_path = data_from_ui(data, signals)
    file_list = glob(f"{input_path}\*.txt")
    file_name = {file.split('\\')[-1].split('.')[0]: file for file in file_list}
    num = get_number_from_file(file_name)
    if not num:
        send_to_ui_status(f'WORNING: 找不到案號檔案')
        return 0

    loose_file = check_file_exist(file_name, num)
    if loose_file:
        send_to_ui_status(f'WORNING: 找不到檔案{loose_file}')
        return 0
    
    output_folder = create_output_path(input_path)
    copy_file(file_list, output_folder)

    total_floor = calculate_start(file_name, output_folder, num)
    send_to_ui_data_send({'num':num, 'floor_num':str(total_floor)})
    send_to_ui_status('轉換完成')
    

def check_file_exist(file_name, num):
    find_file_name = ('INPUT_RCD', 'INPUT_REBAR', 'INPUT_WALLDA', f'{num}INPUT', f'{num}SHEAR')
    loose_file = list()
    for file in find_file_name:
        if file not in file_name:
            loose_file.append(file)

    if len(loose_file):
        return loose_file
    return 0

def get_number_from_file(file_name):
    pattern = re.compile(r"(^[A-Z]\d\d\d)", re.I)
    for file_name in file_name.keys():
        find =pattern.findall(file_name)
        if len(find):
            num = find[0]
            break
    if num:  
        return num
    return 0

def create_output_path(input_path):
    path = '\\'.join(input_path.split('\\')[:-1])
    output_folder = fr"{path}\OUTPUT"
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def copy_file(file_list, output_folder):
    for file in file_list:
        shutil.copy(file, output_folder)


def calculate_start(file_name, output_folder, num):
    for name, path in file_name.items():
        if name == 'INPUT_REBAR':
            output_path = REBAR.transfer_rebar(path, output_folder, num)
            send_to_ui_status(f"生成檔案: {output_path}")
        if name == 'INPUT_RCD':
            output_path = RCD.transfer_rcd(path, output_folder, num)
            send_to_ui_status(f"生成檔案: {output_path}")
        if name == 'INPUT_WALLDA':
            output_path = WALLDA.transfer_wallda(path, output_folder)
            send_to_ui_status(f"生成檔案: {output_path}")
        if name == f'{num}INPUT':
            total_floor, output_list = INDATA.tranfer(path, output_folder, num, FC, HNDL)
            print('total_floor:', total_floor)
            for out in output_list:
                send_to_ui_status(f"生成檔案: {out}")
        
    return total_floor
        

if "__main__" == __name__:
    main_flow(input_path)