import os 
import sys
import numpy as np

#input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\01_REBAR\INPUT_REBAR.txt'

def transfer_rebar(input_path, output_folder, num):

    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))

    full_output_data = ''
    floor_flag = False

    data_list = [i.strip(' ') for i in data.split('\n') if i !='']
    title = data_list[0]
    title_list = [i for i in title.split('\t') if i !='']
    STORY_index = title_list.index('Story')
    BayID_index = title_list.index('BayID')
    StnLoc_index = title_list.index('StnLoc')
    AsTop_index = title_list.index('AsTop')
    AsBot_index = title_list.index('AsBot')

    title_output = (f"Story{' '*(8-len('Story'))}"
                    f"BayID{' '*(8-len('BayID'))}"
                    f"StnLoc{' '*(8-len('StnLoc'))}"
                    f"AsTop{' '*(8-len('AsTop'))}"
                    f"AsBot{' '*(8-len('AsBot'))}\n")

    full_output_data += title_output

    for data_n in data_list[1:]:
        data_n_list = [i for i in data_n.split('\t') if i !='']
        if data_n_list[0] != 'R1F' and not floor_flag:
            continue
        elif data_n_list[0] == 'R1F':
            floor_flag = True

        STORY = str(data_n_list[STORY_index])
        BayID = str(data_n_list[BayID_index])
        StnLoc = str(np.round(float(data_n_list[StnLoc_index]), 1))
        AsTop = str(np.round(float(data_n_list[AsTop_index]), 1))
        AsBot = str(np.round(float(data_n_list[AsBot_index]), 1))

        output_data = (f"{STORY}{' '*(8-len(STORY))}"
                        f"{BayID}{' '*(8-len(BayID))}"
                        f"{StnLoc}{' '*(8-len(StnLoc))}"
                        f"{AsTop}{' '*(8-len(AsTop))}"
                        f"{AsBot}{' '*(8-len(AsBot))}\n")

        full_output_data += output_data 

    output_path = fr"{output_folder}\{num}REBAR.txt"
    with open(output_path, 'w+') as f:
        f.write(full_output_data)   




if __name__ == "__main__":
    transfer_rebar(input_path)

