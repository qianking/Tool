import os 
import sys
import re

input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\INPUT\V600INPUT.txt'

NUM = 'V600'
FC = {1:490, 8:420, 17:350, 23:280}
HNDL = {'1F': 0.8, '3F': 0.9, '15F': 0.8}

def get_story_data(input_path):
    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))

    data_list = [i.strip() for i in data.split('\n \n') if i !='']
    story_data_index = data_list.index('S T O R Y   D A T A')
    #story_title = data_list[story_data_index+1]

    story_data_list = [i.strip() for i in data_list[story_data_index+2].split('\n') if i !='']
    #print(story_data_list)

    return story_data_list

def transfer_fhdd(story_data_list, output_folder):
    full_output_data = ''
    for index, story_data in enumerate(story_data_list):
        if story_data.startswith('R1F'):
            start_index = index
        if story_data.startswith('1F'):
            end_index = index+1
    total_len = end_index- start_index
    total_data = story_data_list[start_index:end_index]
    total_data_str ='\n '.join(total_data)
    full_output_data += f"{total_len}\n "
    full_output_data += total_data_str

    output_path = fr'{output_folder}\FHDD.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)

    return total_data, total_len

def transfer_indata(total_data, output_folder, NUM, FC, HNDL):
    floor_data = []
    for story_data in total_data:
        data = [i.strip() for i in story_data.split(' ') if i !='']
        floor_data.append(data[0])
    
    full_output_data = ''
    tab_times = '\t'*11 + '\n'

    tmp_title = (f"{NUM}.DAI{tab_times}"
                f"#       MATERIALNUMBER{tab_times}"
                f"2{tab_times}"
                f"#       FLOOR   NUMBER{tab_times}"
                f"{len(floor_data)}{tab_times}")
    
    tmp_1 = (f"Es(t/cm^2){tab_times}"
          f"2100{tab_times}"
          f"Fys(t/cm^2){tab_times}"
          f"3.3{tab_times}"
          f"NF      Fc'     Fy      FYS     BMAN    BMAAS   BMIN    BMMIAS  CMAN    CMAAS   CMIN    CMMIAS{tab_times}")
    
    tmp_2 = (f"ANGLE{tab_times}"
            f"90{tab_times}"
            f"TAKE    FLOOR   COLUM{tab_times}"
            f"2{tab_times}"
            f"25{tab_times}"
            f"TAKE    BEAM{tab_times}"
            f"97{tab_times}"
            f"98{tab_times}"
            f"X{tab_times}"
            f"WALL    BEAM{tab_times}"
            f"0{tab_times}"
            f"HNDL{tab_times}")

    tmp_floor_num = ''
    tmp_floor_numB = ''
    tmp_floor_numC = ''
    tmp_fc = ''
    tmp_hndl = ''
    now_fc = 0
    now_hndl = 0
    indataB_pattern = re.compile(r"^(\d)([A-Z])", re.I)

    for i, floor in enumerate(floor_data[::-1], 1):
        tmp_floor_num = f"{floor}{' '*(8-len(floor))}0{tab_times}{tmp_floor_num}" 

        find = indataB_pattern.findall(floor)
        if len(find):
            floor_B = f"{find[0][0]} {find[0][1]}"
            tmp_floor_numB = f"{floor_B}{' '*(8-len(floor_B))}0{tab_times}{tmp_floor_numB}" 
        else:
            tmp_floor_numB = f"{floor}{' '*(8-len(floor))}0{tab_times}{tmp_floor_numB}"

        tmp_floor_numC = f"{floor}{' '*(8-len(floor))}8{tab_times}{tmp_floor_numC}"  

        if FC.get(i):
            now_fc = FC.get(i)
        tmp_fc = f"{str(i)}{' '*(8-len(str(i)))}{now_fc}{' '*(8-len(str(now_fc)))}4200    4200    6       8       6       8       10      8       10      8{tab_times}{tmp_fc}" 

        if HNDL.get(floor):
            now_hndl = HNDL.get(floor)
        tmp_hndl = f"{floor}{' '*(8-len(floor))}{now_hndl}{tab_times}{tmp_hndl}"
    
    #print(tmp_floor_numB)

    full_output_data += tmp_title
    full_output_data += tmp_floor_num
    full_output_data += tmp_1 
    full_output_data += tmp_fc
    full_output_data += tmp_2
    full_output_data += tmp_hndl
   

    output_path = fr'{output_folder}\INDATA.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)

    full_output_data = ''
    full_output_data += tmp_title
    full_output_data += tmp_floor_numB
    full_output_data += tmp_1 
    full_output_data += tmp_fc
    full_output_data += tmp_2
    full_output_data += tmp_hndl
    output_path = fr'{output_folder}\INDATB.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)


    tmp_title = (f"{NUM}.DAI{tab_times}"
                f"#       FLOOR   NUMBER{tab_times}"
                f"{len(floor_data)}{tab_times}")
    full_output_data = ''
    full_output_data += tmp_title
    full_output_data += tmp_floor_numC
    output_path = fr'{output_folder}\INDATC.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)

    
def tranfer(input_path, output_folder, NUM, FC, HNDL):
    story_data_list = get_story_data(input_path)
    total_data, total_floor = transfer_fhdd(story_data_list, output_folder)
    transfer_indata(total_data, output_folder, NUM, FC, HNDL)

    return total_floor


if __name__ == "__main__":
    tranfer(input_path)