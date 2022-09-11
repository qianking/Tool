import os
import sys

input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\INPUT\V600INPUT.txt'

def transfer_point3(input_path):
    with open(input_path, 'r') as f:
        data = f.read()

    full_output_data = ''

    data_list = [i.strip() for i in data.split('\n \n') if i !='']
    point_coordinate_index = data_list.index('P O I N T   C O O R D I N A T E S')
    point_coordinate = data_list[point_coordinate_index+1, point_coordinate_index+3]
    point_coordinate = '\n \n'.join(point_coordinate)


    column_data_index = data_list.index('C O L U M N   C O N N E C T I V I T Y   D A T A')
    column_data = data_list[column_data_index+2]

    beam_data_index = data_list.index('B E A M   C O N N E C T I V I T Y   D A T A')
    beam_data = data_list[beam_data_index+2]




if __name__ == "__main__": 
    a = [1, 2, 3]
    print(a[0:2])   