import os
import datetime
import time
from decimal import Decimal, localcontext
import traceback
import sys
import numpy as np
import re

input_path = r'E:\python\virtualenv\Tool\BCForce\data\ColumnForce data\單位轉換\Force_Data_kgfcm.txt'
upper_path = r'E:\python\virtualenv\Tool\BCForce\data\ColumnForce data\單位轉換'
#input_path = r'E:\python\virtualenv\Tool\BCForce\data\ColumnForce data\INPUT_all.txt'
#upper_path = r'E:\python\virtualenv\Tool\BCForce\data\ColumnForce data'

self = ''
status = ''

def get_variable(**args):
    global input_path
    global upper_path
    global self
    global status

    if 'input_path' in args:
        input_path = args['input_path']
        self = args['self']
        status = args['status']

        upper_path = '\\'.join(input_path.split('\\')[:-1])


def send_to_controller(txt):
    if self != '':
        self.status.emit(txt)


def transfer_data():
    with open(input_path, 'r') as f:
        data = f.read()
    #print(repr(data))
    output_path = ''
    unit_flag = False
    
    if 'Units:Kgf-cm' in data:
        send_to_controller('WORNING! 單位為 : Kgf-cm')
        unit_flag = True

    data_list = [i.strip(' ') for i in data.split('\n \n') if i !='']
    mapping = {value:index for index, value in enumerate(data_list)}
    col_index = mapping.get('C O L U M N   F O R C E S', None)
    beam_index = mapping.get('B E A M   F O R C E S', None)
    #print(col_index, beam_index)
    col_data = None
    beam_data = None
    if col_index and beam_index:
        col_data = data_list[col_index+1 : beam_index-1]
        beam_data= data_list[beam_index+1 :]
    elif col_index:
        col_data = data_list[col_index+1 :]
    elif beam_index:
        beam_data= data_list[beam_index+1 :] 

    path = transfer_col_data(col_data, unit_flag)
    if path:
        output_path += f'{path}\n'

    path = transfer_beam_data(beam_data, unit_flag)
    if path:
        output_path += f'{path}\n'

    return output_path



def transfer_col_data(data_list, unit_flag):
    if data_list:
        full_output_data = ''
        space = 3
        title = data_list[0]
        title_list = [i for i in title.split(' ') if i !='']
        STORY_index = title_list.index('STORY')
        COL_index = title_list.index('COLUMN')
        LOAD_index = title_list.index('LOAD')
        LOC_index = title_list.index('LOC') - 3
        P_index = title_list.index('P') - 3
        V2_index = title_list.index('V2') - 3
        V3_index = title_list.index('V3') - 3
        M2_index = title_list.index('M2') - 3
        M3_index = title_list.index('M3') - 3

        title_output = 'Story' + ' '*space +\
                        'ColumnID' + ' '*space +\
                        'LoadCase' + ' '*space +\
                        'Ln' + ' '*(8-len('Ln')) +' '*space +\
                        'M2,top' + ' '*(8-len('M2,top')) +' '*space +\
                        'M3,top' + ' '*(8-len('M3,top')) +' '*space +\
                        'V2,top' + ' '*(8-len('V2,top')) +' '*space +\
                        'V3,top' + ' '*(8-len('V3,top')) +' '*space +\
                        'P,top' + ' '*(8-len('P,top')) +' '*space +\
                        'M2,bot' + ' '*(8-len('M2,bot')) +' '*space +\
                        'M3,bot' + ' '*(8-len('M3,bot')) +' '*space +\
                        'V2,bot' + ' '*(8-len('V2,bot')) +' '*space +\
                        'V3,bot' + ' '*(8-len('V3,bot')) +' '*space +\
                        'P,bot' + ' '*(8-len('P,bot')) +' '*space + '\n'

        full_output_data += title_output

        if unit_flag:
            title_indice = []
            for i in title_list[3:]:
                o = f" {i}"
                title_indice.append(title.index(o) + len(i) + 1)
            print(title_indice)
        for data_n in data_list[1:]:
            data_n_list = [i for i in data_n.split('\n') if i !='']         #data第一區塊的資料，以\n分割成list
            data_n_title = data_n_list[0]                                   #data第一區塊的資料，的第一行(STORY,BEAM, LOAD)
            data_n_data = data_n_list[1:]                                   #data第一區塊的資料，除了第一行的其他行

            SBL_list = tuple([i for i in data_n_title.split(' ') if i !=''])      #STORY, BEAM, LOAD 在這個區塊中的list
            STORY = SBL_list[STORY_index]
            COL = SBL_list[COL_index]
            LOAD = SBL_list[LOAD_index]
            
            other_list = []
            loc_list = []


            if unit_flag:
                for datas in data_n_data:
                    tmp_data = []
                    len_last = 0
                    for ind in title_indice:
                        ind -= len_last
                        tt = datas[: ind+1]
                        len_last += len(tt)
                        tmp_data.append(float(tt.strip()))
                        datas = datas[ind+1:]
                    
                    other_list.append(tmp_data)
                    loc_list.append(tmp_data[LOC_index])

            else:
                for datas in data_n_data:
                    tmp_data = tuple([float(i) for i in datas.split(' ') if i !=''])
                    other_list.append(tmp_data)
                    loc_list.append(tmp_data[LOC_index])


            
            max_loc_index = loc_list.index(max(loc_list))
            min_loc_index = loc_list.index(min(loc_list))

            Ln = loc_list[max_loc_index] - loc_list[min_loc_index]
            M2_top = other_list[max_loc_index][M2_index]
            M3_top = other_list[max_loc_index][M3_index]
            V2_top = other_list[max_loc_index][V2_index]
            V3_top = other_list[max_loc_index][V3_index]
            P_top = other_list[max_loc_index][P_index]

            M2_bot = other_list[min_loc_index][M2_index]
            M3_bot = other_list[min_loc_index][M3_index]
            V2_bot = other_list[min_loc_index][V2_index]
            V3_bot = other_list[min_loc_index][V3_index]
            P_bot = other_list[min_loc_index][P_index]

            if unit_flag:
                unit_ln = 0.01
                unit_loc = 0.001
                unit_t = 0.00001

                Ln = np.round(Ln*unit_ln, 4)
                P_top = np.round(P_top*unit_loc, 2)
                P_bot = np.round(P_bot*unit_loc, 2)
                V2_top = np.round(V2_top*unit_loc, 2)
                V3_top = np.round(V3_top*unit_loc, 2)
                V2_bot = np.round(V2_bot*unit_loc, 2)
                V3_bot = np.round(V3_bot*unit_loc, 2)
                M2_top = np.round(M2_top*unit_t, 3)
                M3_top = np.round(M3_top*unit_t, 3)
                M2_bot = np.round(M2_bot*unit_t, 3)
                M3_bot = np.round(M3_bot*unit_t, 3)

            output_data = STORY + ' '*(5-len(STORY)) + ' '*space +\
                        COL + ' '*(8-len(COL)) + ' '*space +\
                        LOAD + ' '*(8-len(LOAD)) + ' '*space +\
                        str(Ln) + ' '*(8-len(str(Ln))) + ' '*space +\
                        str(M2_top) + ' '*(8-len(str(M2_top))) + ' '*space +\
                        str(M3_top) + ' '*(8-len(str(M3_top))) + ' '*space +\
                        str(V2_top) + ' '*(8-len(str(V2_top))) + ' '*space +\
                        str(V3_top) + ' '*(8-len(str(V3_top))) + ' '*space +\
                        str(P_top) + ' '*(8-len(str(P_top))) + ' '*space +\
                        str(M2_bot) + ' '*(8-len(str(M2_bot))) + ' '*space +\
                        str(M3_bot) + ' '*(8-len(str(M3_bot))) + ' '*space +\
                        str(V2_bot) + ' '*(8-len(str(V2_bot))) + ' '*space +\
                        str(V3_bot) + ' '*(8-len(str(V3_bot))) + ' '*space +\
                        str(P_bot) + ' '*(8-len(str(P_bot))) + ' '*space +'\n'
                       
            full_output_data += output_data

        return write_file('ColumnForce', full_output_data)
    
                
def transfer_beam_data(data_list, unit_flag):
    if data_list:
        full_output_data = ''
        space = 3
        unusual_beam_list = list()

        title = data_list[0]                                         
        title_list = [i for i in title.split(' ') if i !='']

        STORY_index = title_list.index('STORY')
        BEAM_index = title_list.index('BEAM')
        LOAD_index = title_list.index('LOAD')
        LOC_index = title_list.index('LOC') - 3
        V2_index = title_list.index('V2') - 3
        M3_index = title_list.index('M3') - 3

        title_output = 'Story' + ' '*space +\
                        'BeamID' + ' '*space +\
                        'LoadCase' + ' '*space +\
                        'Ln' + ' '*(8-len('Ln')) +' '*space +\
                        'ML' + ' '*(7-len('ML')) +' '*space +\
                        'MMmax' + ' '*(8-len('MMmax')) +' '*space +\
                        'MMmin' + ' '*(8-len('MMmin')) +' '*space +\
                        'MR' + ' '*(7-len('MR')) +' '*space +\
                        'VL' + ' '*(6-len('VL')) +' '*space +\
                        'VMmax' + ' '*(6-len('VMmax')) +' '*space +\
                        'VMmin' + ' '*(6-len('VMmin')) +' '*space +\
                        'VR' + ' '*(6-len('VR')) +' '*space + '\n'

        full_output_data += title_output

        if unit_flag:
            title_indice = []
            for i in title_list[3:]:
                o = f" {i}"
                title_indice.append(title.index(o) + len(i) + 1)
            print(title_indice)

        for data_n in data_list[1:]:
                                            
            data_n_list = [i for i in data_n.split('\n') if i !='']         #data第一區塊的資料，以\n分割成list
            data_n_title = data_n_list[0]                                   #data第一區塊的資料，的第一行(STORY,BEAM, LOAD)
            data_n_data = data_n_list[1:]                                   #data第一區塊的資料，除了第一行的其他行

            SBL_list = [i for i in data_n_title.split(' ') if i !='']       #STORY, BEAM, LOAD 在這個區塊中的list
            STORY = SBL_list[STORY_index]
            BEAM = SBL_list[BEAM_index]
            LOAD = SBL_list[LOAD_index]

            LOC_list = []
            V2_list = []
            M3_list = []


            if unit_flag:
                for datas in data_n_data:
                    tmp_data = []
                    len_last = 0
                    for ind in title_indice:
                        ind -= len_last
                        tt = datas[: ind+1]
                        len_last += len(tt)
                        tmp_data.append(float(tt.strip()))
                        datas = datas[ind+1:]
                    
                    LOC_list.append(tmp_data[LOC_index])
                    V2_list.append(tmp_data[V2_index])
                    M3_list.append(tmp_data[M3_index])
            else:
                for datas in data_n_data:
                    tmp_data = [float(i) for i in datas.split(' ') if i !='']
                    LOC_list.append(tmp_data[LOC_index])
                    V2_list.append(tmp_data[V2_index])
                    M3_list.append(tmp_data[M3_index])

            Ln = float(Decimal(str(LOC_list[-1])) - Decimal(str(LOC_list[0])))
            ML = M3_list[0]
            MR = M3_list[-1]
            VL = V2_list[0]
            VR = V2_list[-1]

            with localcontext() as ctx:
                ctx.prec = 5
                perid = Decimal(Ln)/Decimal('4')
                

            START_num = float(Decimal(str(LOC_list[0])) + perid)
            
            END_num = float(Decimal(str(LOC_list[-1])) - perid)
            

            for num in LOC_list:
                if START_num <= num:
                    START_index = LOC_list.index(num) 
                    break

            for i, num in enumerate(LOC_list[::-1]):
                if END_num >= num:
                    END_index = i
                    END_index = len(LOC_list) - END_index - 1 
                    break

            #print('START_index = ', START_index)
            #print('END_index = ', END_index)

            MM_list = M3_list[START_index : END_index +1]
            VM_list = V2_list[START_index : END_index +1]
            #print('MM_list=', MM_list)
            #print('VM_list=', VM_list)

            if len(M3_list) == 2:
                MM_list = M3_list
                VM_list = V2_list
                if f"{STORY}  {BEAM}" not in unusual_beam_list:
                    unusual_beam_list.append(f"{STORY}  {BEAM}")

            MMmax = max(MM_list)
            if MMmax < 0: 
                MMmax = 0
            MMmin = min(MM_list)
            if MMmin > 0: 
                MMmin = 0

            VMmax = max(VM_list)
            if VMmax < 0: 
                VMmax = 0

            VMmin = min(VM_list)
            if VMmin > 0: 
                VMmin = 0
            
            if unit_flag:
                unit_loc = 0.01
                unit_m = 0.00001
                unit_v = 0.001
                Ln = np.round(Ln*unit_loc, 4)
                ML = np.round(ML*unit_m, 3)
                MR = np.round(MR*unit_m, 3)
                VL = np.round(VL*unit_v, 2)
                VR = np.round(VR*unit_v, 2)
                MMmax = np.round(MMmax*unit_m, 3)
                MMmin = np.round(MMmin*unit_m, 3)
                VMmax = np.round(VMmax*unit_v, 2)
                VMmin = np.round(VMmin*unit_v, 2)

            output_data = STORY + ' '*(5-len(STORY)) + ' '*space +\
                        BEAM + ' '*(6-len(BEAM)) + ' '*space +\
                        LOAD + ' '*(8-len(LOAD)) + ' '*space +\
                        str(Ln) + ' '*(8-len(str(Ln)))  + ' '*space +\
                        str(ML) + ' '*(7-len(str(ML)))  + ' '*space +\
                        str(MMmax) + ' '*(8-len(str(MMmax)))  + ' '*space +\
                        str(MMmin) + ' '*(8-len(str(MMmin)))  + ' '*space +\
                        str(MR) + ' '*(7-len(str(MR)))  + ' '*space +\
                        str(VL) + ' '*(6-len(str(VL)))  + ' '*space +\
                        str(VMmax) + ' '*(6-len(str(VMmax)))  + ' '*space +\
                        str(VMmin) + ' '*(6-len(str(VMmin)))  + ' '*space +\
                        str(VR) + ' '*(6-len(str(VR)))  + ' '*space + '\n'


            full_output_data += output_data
        
        if len(unusual_beam_list):
            unusual_beam = '\n'.join(unusual_beam_list)
    
            send_to_controller(f'警告! 樑力量整理異常: \n{unusual_beam}')

        return write_file('BeamForce', full_output_data)
    
    

def write_file(output_name, full_output_data):
    txtfile_list = [f for f in os.listdir(upper_path) if '.txt' in f]
    output_file_name = f"{output_name}.txt"
    repeat_times = 0

    while True:
        repeat_times += 1
        if output_file_name in txtfile_list:
            output_file_name = f"{output_name}_{repeat_times}.txt"
        else:
            break
    
    output_path = os.path.join(upper_path, output_file_name)
    #print(output_path)
    
    with open(output_path, 'w+') as f:
        f.write(full_output_data)
    return output_path


def timer_and_debug(func):
    def warpper(*args, **wargs):
        try:
            send_to_controller('Start Transfer...')
            start = time.time()
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
            send_to_controller(f'Error:{errMsg}')
        else:
            end = time.time()
            cost_time = str(end- start)
            cost_time = cost_time[:4]
            send_to_controller(f'Transfer Done! \nCost {cost_time}s \nOutput path:\n{output_path}')
    return warpper

@timer_and_debug
def main(**args):
    get_variable(**args)
    output_path = transfer_data()
    return output_path
    




if "__main__" == __name__:
    #transfer_beam_data()
    #transfer_data()
    main()
    #print(np.round(0.00994, 3))



















