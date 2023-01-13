import os 
import sys
import re

input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\INPUT\V600INPUT.txt'
output_folder = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\OUTPUT_TEST'

NUM = 'V600'
FC = {1:490, 8:420, 17:350, 23:280}
HNDL = {'1F': 0.8, '3F': 0.9, '15F': 0.8}

def get_story_data(input_path):
    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))

    data_list = [i for i in data.split('\n \n') if i !='']
    for i, dd in enumerate(data_list):
        if 'S T O R Y   D A T A' in dd:
            story_data_index = i

    story_data_list = [i for i in data_list[story_data_index+2].split('\n') if i !='']
    for index, story_data in enumerate(story_data_list):
        if story_data.strip().startswith('R1F'):
            start_index = index
        if story_data.strip().startswith('1F'):
            end_index = index+1
    total_floor = end_index - start_index
    story_data_list = story_data_list[start_index:end_index]

    return story_data_list, total_floor

def transfer_fhdd(story_data_list, total_floor, output_folder):
    full_output_data = ''
    
    total_story_data ='\n'.join(story_data_list)
    full_output_data += f"{total_floor}\n"
    full_output_data += total_story_data

    output_fhdd_path = fr'{output_folder}\FHDD.txt'
    with open(output_fhdd_path, 'w+') as f:
        f.write(full_output_data)

    return output_fhdd_path

def transfer_indatabc(story_data_list, output_folder, NUM, FC, HNDL):
    floor_data = []
    for story_data in story_data_list:
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

        if FC.get(floor):
            now_fc = FC.get(floor)
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
   

    output_A_path = fr'{output_folder}\INDATA.txt'
    with open(output_A_path, 'w+') as f:
        f.write(full_output_data)

    full_output_data = ''
    full_output_data += tmp_title
    full_output_data += tmp_floor_numB
    full_output_data += tmp_1 
    full_output_data += tmp_fc
    full_output_data += tmp_2
    full_output_data += tmp_hndl
    output_B_path = fr'{output_folder}\INDATB.txt'
    with open(output_B_path, 'w+') as f:
        f.write(full_output_data)


    tmp_title = (f"{NUM}.DAI{tab_times}"
                f"#       FLOOR   NUMBER{tab_times}"
                f"{len(floor_data)}{tab_times}")
    full_output_data = ''
    full_output_data += tmp_title
    full_output_data += tmp_floor_numC
    output_C_path = fr'{output_folder}\INDATC.txt'
    with open(output_C_path, 'w+') as f:
        f.write(full_output_data)
    
    return output_A_path, output_B_path, output_C_path


def transfer_point3(input_path, output_folder):
    with open(input_path, 'r') as f:
        data = f.read()

    full_output_data = ''

    data_list = [i for i in data.split('\n \n') if i !='']

    for i, dd in enumerate(data_list):
        if 'P O I N T   C O O R D I N A T E S' in dd:
            point_coordinate_index = i
        if 'C O L U M N   C O N N E C T I V I T Y   D A T A' in dd:
            column_data_index = i
        if 'B E A M   C O N N E C T I V I T Y   D A T A' in dd:
            beam_data_index = i
    
    point_coordinate = data_list[point_coordinate_index+1: point_coordinate_index+3]
    point_coordinate = '\n \n'.join(point_coordinate)
    point_coordinate = point_coordinate.strip('\n')
    #print(point_coordinate)

    column_data = data_list[column_data_index+2]

    beam_data = data_list[beam_data_index+1: beam_data_index+3]
    beam_data = '\n \n'.join(beam_data)
    beam_data = beam_data.strip('\n')
    #print(repr(beam_data))
    
    full_output_data += f'{point_coordinate}\n'
    full_output_data += '9999\n'
    full_output_data += 'COL\n'
    full_output_data += f'{column_data}\n'
    full_output_data += '9999\n'
    full_output_data += f'{beam_data}\n'
    full_output_data += '9999'
    
    output_point_path = fr"{output_folder}\POINT3.txt"
    with open(output_point_path, 'w+') as f:
        f.write(full_output_data)
    
    return output_point_path

    
def get_floor_data(input_path):
    story_data_list, total_floor = get_story_data(input_path)
    floor_list = []
    for story_data in story_data_list:
        data = [i.strip() for i in story_data.split(' ') if i !='']
        floor_list.append(data[0])
    return total_floor, floor_list

def tranfer(input_path, output_folder, data):
    story_data_list, total_floor = get_story_data(input_path)
    output_fhdd = transfer_fhdd(story_data_list, total_floor, output_folder)
    output_A_path, output_B_path, output_C_path = transfer_indatabc(story_data_list, output_folder, data['num'], data['FC'], data['HNDL'])
    output_point_path = transfer_point3(input_path, output_folder)
    output_list = [output_fhdd, output_A_path, output_B_path, output_C_path, output_point_path] 
    return output_list


if __name__ == "__main__":
    tranfer(input_path, output_folder, NUM, FC, HNDL)