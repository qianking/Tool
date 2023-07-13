import os 
import sys
import numpy as np
import re

input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\03_WALLDA\INPUT_WALLDA.txt'

def transfer_wallda(input_path, output_folder):

    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))
    
    full_output_data = ''
    floor_flag = False

    data_list = [i.strip(' ') for i in data.split('\n') if i !='']
    title = data_list[0]
    title_list = [i for i in title.split('\t') if i !='']

    STORY_index = title_list.index('Story')
    Pier_index = title_list.index('Pier')
    Load_index = title_list.index('Load')
    Loc_index = title_list.index('Loc')
    V2_index = title_list.index('V2')
    V3_index = title_list.index('V3')

    title_output = (f"Story{' '*(10-len('Story'))}"
                    f"Pier{' '*(10-len('Pier'))}"
                    f"Load{' '*(10-len('Load'))}"
                    f"Loc{' '*(10-len('Loc'))}"
                    f"V2{' '*(10-len('V2'))}"
                    f"V3{' '*(10-len('V3'))}\n")
    full_output_data += title_output

    #找到第一列data中的pier編號
    data_1_list = [i for i in data_list[1].split('\t') if i !='']
    Pier_1 = data_1_list[Pier_index]
    pattern = re.compile(r'([A-Z])(\d+)', re.I)
    find_data = pattern.findall(Pier_1)
    frist_en_len = len(find_data[0][0])
    now_num = int(Pier_1[frist_en_len:])
    now_pier = Pier_1

    for data_n in data_list[1:]:
        data_n_list = [i for i in data_n.split('\t') if i !='']
        STORY = str(data_n_list[STORY_index])
        Pier = str(data_n_list[Pier_index])
        Load = str(data_n_list[Load_index])
        Loc = str(data_n_list[Loc_index])
        V2 = str(data_n_list[V2_index])
        V3 = str(data_n_list[V3_index])

        if Pier != now_pier:   #如果Pier跟上一個不同，就代表進入下一區域，那flag就要歸位
            now_pier = Pier
            floor_flag = False

        if data_n_list[0] != 'R1F' and not floor_flag:
            continue
        elif data_n_list[0] == 'R1F':
            floor_flag = True
        
        output_data = (f"{STORY}{' '*(10-len(STORY))}"
                        f"{Pier}{' '*(10-len(Pier))}"
                        f"{Load}{' '*(10-len(Load))}"
                        f"{Loc}{' '*(10-len(Loc))}"
                        f"{V2}{' '*(10-len(V2))}"
                        f"{V3}{' '*(10-len(V3))}\n")
    
        full_output_data += output_data

        output_path = fr"{output_folder}\WALLDA.txt"
        #output_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\03_WALLDA\WALLDA_Test.txt'
        with open(output_path, 'w+') as f:
            f.write(full_output_data) 
            
    return output_path  
        

if __name__ == "__main__":
    transfer_wallda(input_path, output_folder)
