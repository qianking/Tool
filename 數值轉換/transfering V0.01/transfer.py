import os
import datetime
import time
from decimal import Decimal, localcontext
import traceback
import sys


input_path = r'E:/python/Numerical extraction/data/input_test.txt'
self = ''
status = ''

def get_variable(**args):
    global input_path
    global self
    global status

    if 'input_path' in args:
        input_path = args['input_path']
        input_path = input_path.replace('/', '\\')
        self = args['self']
        status = args['status']

def send_to_controller(txt):
    if self != '':
        self.status.emit(txt)

def transfer_data():
    with open(input_path, 'r') as f:
        data = f.read()

    full_output_data = ''
    space = 3
   
    data_list = [i.strip(' ') for i in data.split('\n \n') if i !='']        #將得到的data以\n \n分割
    BeamForce_index = data_list.index('B E A M   F O R C E S')
    data_list = data_list[BeamForce_index+1:]
    title = data_list[0]                                         
    title_list = [i for i in title.split(' ') if i !='']
    print('title_list = ', title_list)

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
        for datas in data_n_data:
            tmp_data = [float(i) for i in datas.split(' ') if i !='']
            LOC_list.append(tmp_data[LOC_index])
            V2_list.append(tmp_data[V2_index])
            M3_list.append(tmp_data[M3_index])

        Ln = str(Decimal(str(LOC_list[-1])) - Decimal(str(LOC_list[0])))
        ML = str(M3_list[0])
        MR = str(M3_list[-1])
        VL = str(V2_list[0])
        VR = str(V2_list[-1])

        with localcontext() as ctx:
            ctx.prec = 5
            perid = Decimal(Ln)/Decimal('4')
            

        START_num = float(Decimal(str(LOC_list[0])) + perid)
        
        END_num = float(Decimal(str(LOC_list[-1])) - perid)
        

        for num in LOC_list:
            if START_num <= num:
                START_index = LOC_list.index(num) 
                break

        for num in LOC_list[::-1]:
            if END_num >= num:
                END_index = LOC_list[::-1].index(num)
                END_index = len(LOC_list) - END_index -1 
                break

        #print('START_index = ', START_index)
        #print('END_index = ', END_index)

        MM_list = M3_list[START_index:END_index +1]
        VM_list = V2_list[START_index:END_index +1]
        #print('MM_list=', MM_list)
        #print('VM_list=', VM_list)

        MMmax = max(MM_list)
        if MMmax < 0: MMmax = str(0) 
        else: MMmax = str(MMmax)
        MMmin = min(MM_list)
        if MMmin > 0: MMmin = str(0) 
        else: MMmin = str(MMmin)

        VMmax = max(VM_list)
        if VMmax < 0: VMmax = str(0) 
        else: VMmax = str(VMmax)

        VMmin = min(VM_list)
        if VMmin > 0: VMmin = str(0)
        else: VMmin = str(VMmin)

        output_data = STORY + ' '*(5-len(STORY)) + ' '*space +\
                    BEAM + ' '*(6-len(BEAM)) + ' '*space +\
                    LOAD + ' '*(8-len(LOAD)) + ' '*space +\
                    Ln + ' '*(8-len(Ln))  + ' '*space +\
                    ML + ' '*(7-len(ML))  + ' '*space +\
                    MMmax + ' '*(8-len(MMmax))  + ' '*space +\
                    MMmin + ' '*(8-len(MMmin))  + ' '*space +\
                    MR + ' '*(7-len(MR))  + ' '*space +\
                    VL + ' '*(6-len(VL))  + ' '*space +\
                    VMmax + ' '*(6-len(VMmax))  + ' '*space +\
                    VMmin + ' '*(6-len(VMmin))  + ' '*space +\
                    VR + ' '*(6-len(VR))  + ' '*space + '\n'


        full_output_data += output_data
    
    output_path = write_file(input_path, full_output_data)
    return output_path
    

def write_file(input_path, full_output_data):
    today = str(datetime.date.today())
    path = input_path.split('\\')
    path = path[:-1]
    path = '\\'.join(path)
    print(path)

    txtfile_list = [f for f in os.listdir(path) if '.txt' in f]
    #print(txtfile_list)
    output_file_name = f"{today}_output.txt"

    repeat_times = 0
    while True:
        repeat_times += 1
        if output_file_name in txtfile_list:
            output_file_name = f"{today}_output_{repeat_times}.txt"
        else:
            break

    output_path = os.path.join(path, output_file_name)
    print(output_file_name)
    
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
            send_to_controller(f'Exception:{errMsg}')
        else:
            end = time.time()
            cost_time = str(end- start)
            cost_time = cost_time[:4]
            send_to_controller(f'Transfer Done! \nCost {cost_time}s \nOutput path:{output_path}')
    return warpper



@timer_and_debug
def main(**args):
    get_variable(**args)
    output_path = transfer_data()
    return output_path
    
    




if "__main__" == __name__:
    transfer_data()



















