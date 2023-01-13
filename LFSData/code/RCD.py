import os 
import sys
import numpy as np

input_path = r'C:\Users\Qian\Downloads\V624_INPUT\INPUT\INPUT_RCD.txt'
output_folder = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\output_tet'

def transfer_rcd(input_path, output_folder, num):

    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))

    full_output_data = ''
    floor_flag = False

    data_list = [i.strip(' ') for i in data.split('\n') if i !='']
    title = data_list[0]
    #print('title', title)
    title_list = [i for i in title.split('\t') if i !='']
    STORY_index = title_list.index('Story')
    Line_index = title_list.index('Line')
    Line_type = title_list.index('LineType')
    AnalysisSect_index = title_list.index('AnalysisSect')

    title_output = (f"Story{' '*(10-len('Story'))}"
                    f"Line{' '*(10-len('Line'))}"
                    f"AnalysisSect{' '*(40-len('AnalysisSect'))}\n")

    full_output_data += title_output

    for data_n in data_list[1:]:
        data_n_list = [i for i in data_n.split('\t') if i !='']       
        if data_n_list[Line_type] != "Column" and data_n_list[Line_type] != "Beam":
            continue
        if data_n_list[STORY_index] != 'R1F' and not floor_flag:
            continue
        elif data_n_list[STORY_index] == 'R1F':
            floor_flag = True

        STORY = str(data_n_list[STORY_index])
        Line = str(data_n_list[Line_index])
        AnalysisSect = str(data_n_list[AnalysisSect_index])
        

        output_data = (f"{STORY}{' '*(10-len(STORY))}"
                        f"{Line}{' '*(10-len(Line))}"
                        f"{AnalysisSect}{' '*(40-len(AnalysisSect))}\n")

        full_output_data += output_data 

    output_path = fr"{output_folder}\{num}RCD.txt"
    with open(output_path, 'w+') as f:
        f.write(full_output_data) 
    return output_path 

def read_output(output_path): #驗證用
    with open(output_path, 'r') as f:
        data = f.read()
    print(repr(data))

if __name__ == "__main__":
    transfer_rcd(input_path, output_folder, 'V650')
