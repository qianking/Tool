import os 
import sys

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
    story_title = data_list[story_data_index+1]

    story_data_list = [i.strip() for i in data_list[story_data_index+2].split('\n') if i !='']
    print(story_data_list)

    

    return story_data_list

def transfer_fhdd(story_data_list):
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

    output_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\OUTPUT_TEST\FHDD.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)

    return total_data 

def transfer_indata(total_data):
    floor_data = []
    for story_data in total_data:
        data = [i.strip() for i in story_data.split(' ') if i !='']
        floor_data.append(data[0])
    
    full_output_data = ''
    tab_times = '\t'*11 + '\n'

    full_output_data = (f"{NUM}.DAI{tab_times}"
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
    tmp_fc = ''
    tmp_hndl = ''
    now_fc = 0
    now_hndl = 0

    for i, floor in enumerate(floor_data[::-1], 1):
        tmp_floor_num = f"{floor}{' '*(8-len(floor))}0{tab_times}{tmp_floor_num}"  

        if FC.get(i):
            now_fc = FC.get(i)
        tmp_fc = f"{str(i)}{' '*(8-len(str(i)))}{now_fc}{' '*(8-len(str(now_fc)))}4200    4200    6       8       6       8       10      8       10      8{tab_times}{tmp_fc}" 

        if HNDL.get(floor):
            now_hndl = HNDL.get(floor)
        tmp_hndl = f"{floor}{' '*(8-len(floor))}{now_hndl}{tab_times}{tmp_hndl}"
    
    full_output_data += tmp_floor_num
    full_output_data += tmp_1 
    full_output_data += tmp_fc
    full_output_data += tmp_2
    full_output_data += tmp_hndl
   

    output_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\OUTPUT_TEST\INDATA.txt'
    with open(output_path, 'w+') as f:
        f.write(full_output_data)
    

    
    







def tranfer(input_path):
    story_data_list = get_story_data(input_path)
    total_data = transfer_fhdd(story_data_list)
    transfer_indata(total_data)


if __name__ == "__main__":
    tranfer(input_path)