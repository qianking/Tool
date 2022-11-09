import os
import sys
import random
import traceback

input_path = r'C:\Users\andy_chien\Downloads\V125_A_111.08.08.txt'
output_path = r'C:\Users\andy_chien\Downloads\test-1.txt'

ui_signal = None

def send_to_ui_status(txt):
    ui_signal.status.emit(txt)

def data_from_ui(signals):
    global ui_signal
    ui_signal = signals


def debug(func):
    def warpper(*args, **wargs):
        try:
            output_path = func(*args, **wargs)
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
        else:
            send_to_ui_status('轉換完成')
            send_to_ui_status(f'OUTPUT PATH: {output_path}')
    return warpper


def transfer(input_path):
    replace_name = ('Beam/Column capacity ratio exceeds limit', 
                    'Shear stress due to shear force and torsion together exceeds maximum allowed',
                    'Reinforcing required exceeds maximum allowed', 
                    'Joint shear ratio exceeds limit',
                    'Shear stress exceeds maximum allowed')

    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))
    
    data_list = data.split('\n')
    error_index_dic = dict()
    continue_flag = False
    for i, dd in enumerate(data_list):
        continue_flag = False
        for name in replace_name:
            if name in dd:
                continue_flag = True
                error_index_dic[i] = dd.replace(name, '').rstrip()
                break
            
        if (not continue_flag) and len(error_index_dic):
            random_data = find_same_len(data_list[list(error_index_dic.keys())[0]-30: list(error_index_dic.keys())[0]], len(error_index_dic))
            for i, j in enumerate(error_index_dic):
                ddd = error_index_dic[j] + random_data[i][len(error_index_dic[j]):]
                data_list[j] = ddd
            error_index_dic.clear()
    
    full_data = '\n'.join(data_list)


    output_path = fr"{input_path.split('.')[0]}OUTPUT.txt"
    with open(output_path, 'w+') as f:
        f.write(full_data)
    return output_path


def find_same_len(data_n_list, random_num):
    data_random_list = list()
    len_list = [len(i.rstrip()) for i in data_n_list]
    len_set = tuple(set(len_list))
    len_dic = {len_list.count(len_data) : len_data for len_data in len_set}
    max_len_count = max(list(len_dic.keys()))
    max_len = len_dic[max_len_count]
    for i in data_n_list:
        if len(i.rstrip()) == max_len:
            data_random_list.append(i)
    
    random_data = random.sample(data_random_list, random_num)
    return random_data


#@debug
def Transfer_Flow(input_path, signals=None):
    data_from_ui(signals)
    output_path = transfer(input_path)
    return output_path











if "__main__" == __name__:
    Transfer_Flow(input_path)