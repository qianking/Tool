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
from for_UI_enum import Text_Color

input_path = r'C:\Users\andy_chien\Downloads\弱層資料整理_1\弱層資料整理\INPUT'
output_path = r'C:\Users\andy_chien\Downloads\弱層資料整理_1\弱層資料整理\OUTPUT_TEST'
FC = {1:490, 8:420, 17:350, 23:280}
HNDL = {'1F': 0.8, '3F': 0.9, '15F': 0.8}

ui_show = None

class UI_SHOW():
    def __init__(self, ui_signal):
        self.ui_signal = ui_signal

    def floordata_send(self, floor_data:list):
        if self.ui_signal:
            self.ui_signal.floor_data_send.emit(floor_data)

    def show_status(self, txt, color=Text_Color.black.value):
        if self.ui_signal:
            self.ui_signal.status.emit((txt, color))
    
    def show_result(self, data:dict):
        if self.ui_signal:
            self.ui_signal.result_send.emit(data)
    
    def reset_all(self):
        if self.ui_signal:
            self.ui_signal.reset_all.emit()

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
            ui_show.show_status(f'Error: {errMsg}', Text_Color.red.value)
            ui_show.reset_all()
    return warpper


@debug
def Get_FloorData_Flow(data, signals = None):
    global ui_show
    ui_show = UI_SHOW(signals)
    num = Check_File(data['file_name_dic'])

    total_floor, floor_list = INDATA.get_floor_data(data['file_name_dic'][f'{num}INPUT'])

    ui_show.show_result({'num':num, 'floor_num':str(total_floor)})
    ui_show.floordata_send(floor_list)


@debug   
def Main_Flow(data, signals=None):
    global ui_show
    ui_show = UI_SHOW(signals)
    output_folder = create_output_path(data['input_path'])
    copy_file(data['file_list'], output_folder)

    calculate_start(data, output_folder)
    
    ui_show.show_status('轉換完成!')

def Check_File(file_name_dic):
    num = get_number_from_file(file_name_dic)
    if not num:
        ui_show.show_status(f"WORNING: 找不到 '案號INPUT' 檔案", Text_Color.red.value)
        ui_show.reset_all()
        return 0

    loose_file = check_file_exist(file_name_dic, num)
    if loose_file:
        ui_show.show_status(f'WORNING: 找不到檔案 {loose_file}', Text_Color.red.value)
        ui_show.reset_all()
        return 0
    
    return num

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
    return False

def create_output_path(input_path):
    path = '\\'.join(input_path.split('\\')[:-1])
    output_folder = fr"{path}\OUTPUT"
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def copy_file(file_list, output_folder):
    for file in file_list:
        shutil.copy(file, output_folder)


def calculate_start(data, output_folder):
    for name, path in data['file_name_dic'].items():
        if name == 'INPUT_REBAR':
            output_path = REBAR.transfer_rebar(path, output_folder, data['num'])
            ui_show.show_status(f"生成檔案: {output_path}", Text_Color.blue.value)
        if name == 'INPUT_RCD':
            output_path = RCD.transfer_rcd(path, output_folder, data['num'])
            ui_show.show_status(f"生成檔案: {output_path}", Text_Color.blue.value)
        if name == 'INPUT_WALLDA':
            output_path = WALLDA.transfer_wallda(path, output_folder)
            ui_show.show_status(f"生成檔案: {output_path}", Text_Color.blue.value)
        if name == f"{data['num']}INPUT":
            output_list = INDATA.tranfer(path, output_folder, data)
            for out in output_list:
                ui_show.show_status(f"生成檔案: {out}", Text_Color.blue.value)
        
        

if "__main__" == __name__:
    Main_Flow(input_path)