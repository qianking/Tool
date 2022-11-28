import subprocess
import os
import subprocess as sp
import sys
sys.path.append(r"C:\littleTooldata\IPLAS\program\my lib")
import file_util

path = r"C:\littleTooldata\IPLAS\Schedule_data\data"
Set_schedule_path = r"C:\littleTooldata\IPLAS\Schedule_data\Set_Schedule.ps1"
Del_schedule_path = r"C:\littleTooldata\IPLAS\Schedule_data\Del_schedule.ps1"
IPLAS_log_path = "C:\littleTooldata\IPLAS\logs"
Set_Schedular_logger = file_util.create_logger(IPLAS_log_path, 'Set_Schedular_log')

execute_dict = {'All_project': ['SWITCH_CISCO_EZ1KA1', 'UC_POLY_MTR', 'UC_UNIFY_CP700', 'EZ1K_A2_ACT2', 'SWITCH_YAMAHA_BLUES'], 'Select_project': ['SWITCH_CISCO_EZ1KA1', 0], 'Time_set': ['Current shift', 0], 'Check_box_default': [1, 1, 1], 'Download_path': 'C:\\littleTooldata\\IPLAS\\Download', 'Set_schedular_time': '09:30'}

def create_file():
    if not os.path.exists(path):
        os.makedirs(path)

def get_str(name_temp):
    for i in range(len(name_temp)):
        if i == 0:
            name =  str(name_temp[i]).replace(" ", "_")
        else: 
            name = name + " " + str(name_temp[i]).replace(" ", "_")
    return name

#bat_name : selecttime_scheduletime_project.bat
def set_scheduler(execute_dict):
    #讀取數據
    create_file()
    data = execute_dict
    #print(data)
    selecttime_temp = data["Time_set"]
    scheduletime = data['Set_schedular_time']
    project_temp = data["Select_project"]
    if_pass_fail_temp = data["Check_box_default"]
    doenload_path = data["Download_path"]
    All_project_temp = data["All_project"]
    
    datetime = selecttime_temp[2]
    Input_datetime = datetime.split(' ')[0].strip() + "_" + datetime.split(' ')[1].strip() + '+' + datetime.split(' ')[-2].strip() + "_" + datetime.split(' ')[-1].strip()
    selecttime_temp[2] = Input_datetime
    
    All_project = get_str(All_project_temp)
    project = get_str(project_temp)
    selecttime = get_str(selecttime_temp)
    if_pass_fail = get_str(if_pass_fail_temp)
    
    #得到bat檔案名稱
    time_select = selecttime_temp[0].replace(' ', '_')
    selecproject = project_temp[0]
    time = scheduletime.replace(':', '-')
    
    file_name = f"{time_select}_{time}_{selecproject}.bat"
    #print(file_name)
    bat_path = f"{path}\{file_name}"

    if os.path.exists(bat_path):
        Set_Schedular_logger.info(f'[{file_name}] This Schedular Setting Exists!')
        return None, "This Schedular Setting Exists!"
    else:
        with open(bat_path,'a+') as f:     
            f.write(f"@echo off\ncd C:\littleTooldata\IPLAS\program\my lib\npython Download_isn.py -all {All_project} -pro {project} -time {selecttime} -check {if_pass_fail} -path {doenload_path}")
        info = call_sch(file_name, scheduletime)
        if 'Ready' in str(info):
            Set_Schedular_logger.info(f'[{file_name}] Schedular Setup Complete')
            return file_name, "Schedular Setup Complete"
        else:
            return None, "Setting Schedular Failed!"


def del_scheduler(file_name):
    info = del_sch(file_name)
    bat_path = f"{path}\{file_name}"
    if os.path.exists(bat_path):
        os.remove(bat_path)
    if 'sucess delete' in str(info):
        Set_Schedular_logger.info(f'Success Delete Schedular [{file_name}]')
        return "Success Delete Schedular"
    if 'no such schedular setup' in str(info):
        return "No Such Schedular Setup"
    

def call_sch(file_name, scheduletime):
    name = file_name.split('.')[0]
    try:
        args=[r"C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe","-ExecutionPolicy","Unrestricted", Set_schedule_path, name, scheduletime, file_name,path]
        p=subprocess.Popen(args, stdout=subprocess.PIPE)
        dt=p.stdout.read()
        #print(dt)
        return dt
    except Exception as e:
        Set_Schedular_logger.info(f'[{file_name}] Setting Schedular Failed!  erro:{str(e)}')
    return False

def del_sch(file_name):
    name = file_name.split('.')[0]
    try:
        args=[r"C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe","-ExecutionPolicy","Unrestricted", Del_schedule_path, name]
        p=subprocess.Popen(args, stdout=subprocess.PIPE)
        dt=p.stdout.read()
        return dt
    except Exception as e:
        Set_Schedular_logger.info(f'No Such Schedular Setup [{file_name}]  error: {str(e)}')
    return False


if __name__ == '__main__':
    #call_sch()
    set_scheduler(execute_dict = {'All_project': ['SWITCH_CISCO_EZ1KA1', 'UC_POLY_MTR', 'UC_UNIFY_CP700', 'EZ1K_A2_ACT2', 'SWITCH_YAMAHA_BLUES'], 'Select_project': ['SWITCH_CISCO_EZ1KA1', 0], 'Time_set': ['Current shift', 0], 'Check_box_default': [1, 1, 1], 'Download_path': 'C:\\littleTooldata\\IPLAS\\Download', 'Set_schedular_time': '09:30'})