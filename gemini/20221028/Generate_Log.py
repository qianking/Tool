import os 
from datetime import datetime
from copy import deepcopy
from Global_Variable import SingleTon_Global

log_root_path = '.\\log'
os.makedirs(log_root_path, exist_ok=True) 
class DrawStringLogWithChinese():

    def __init__(self, threal_local):
        """
        畫圖表(可使用中文字體)，回傳String
        """

        self.raw_data_list = threal_local.form_log

    def _StringLengthCount(self, InputString):
        """
        字串長度分析(中文:2,英文:1)
        """
        count = 0
        for string in InputString:
            if u'\u4e00' <= string <= u'\u9fff':
                count += 2
            else:
                count += 1
        return count

    def __repr__(self):
        LinesItemLen = len(self.raw_data_list)  # 找出總共有多少行
        LineItemLen = len(self.raw_data_list[0])  # 找出第一行共有幾個項目
        ItemMaxLength = []
        MaxWidth = 0
        MaxHight = 0
        ItemIndex = 0
        NewLine = "\r\n"
        TmpLog = ""

        for i in range(LinesItemLen):  # 總共要跑多少行且找出Item最長的長度
            if i == 0:  # 第一行
                for j in range(LineItemLen):
                    ItemMaxLength.append(self._StringLengthCount(self.raw_data_list[i][j]))  # 加入
            else:  # 第二行以後
                for j in range(LineItemLen):
                    currentLen = self._StringLengthCount(self.raw_data_list[i][j])
                    if currentLen > ItemMaxLength[j]:  # 比較長度
                        ItemMaxLength[j] = currentLen

        for i in range(LineItemLen):  # 加總項目總長度
            MaxWidth += ItemMaxLength[i]

        MaxWidth = MaxWidth+(LineItemLen*3)+1  # 最大的寬度
        MaxHight = (LinesItemLen*2)+1  # 最大的高度

        for i in range(MaxHight):
            if (i % 2) == 0:  # 單號排(1,3,5,7,......)
                for j in range(MaxWidth):
                    if ((i == MaxHight - 1) and (j == 0)) or ((i == MaxHight-1) and (j == MaxWidth-1)):
                        TmpLog += "="
                    elif((i != 0) and (j == 0)) or ((i != 0) and (j == MaxWidth-1)):
                        TmpLog += "|"
                    else:
                        TmpLog += "="
                TmpLog += NewLine
            else:  # 雙號排(2,4,6,8,......)
                ItemIndex = (int)(i-(int)(i/2)-1)
                for j in range(LineItemLen):
                    TmpLog += "| "
                    TmpLog += self.raw_data_list[ItemIndex][j]
                    TmpLog += " "
                    for Space in range(ItemMaxLength[j]-self._StringLengthCount(self.raw_data_list[ItemIndex][j])):
                        TmpLog += " "
                TmpLog += "|"
                TmpLog += NewLine
        return TmpLog


class Log_Title():
    
    v = SingleTon_Global()

    def __init__(self, threal_local, thread_global):
        """
        傳回log title的資料
        """
        self._title_data = {'program_version' : threal_local.VERSION, 
                    'test_result' : "PASS" if not threal_local.dut_test_fail else "FAIL",
                    'error_code' : threal_local.error_code,
                    'csn' : threal_local.dut_info.get('SN'),
                    'start_time' : thread_global.test_start_time,
                    'end_time' : thread_global.test_end_time}
        

    def __repr__(self):
        temp_str = str()
        for name, data in self._title_data.items():
            temp_str += f"{name} : {data}\r\n"
        return temp_str.strip()


class Gearate_log():

    v = SingleTon_Global()

    def __init__(self, threal_local, thread_global):
        self.threal_local = threal_local
        self.thread_global = thread_global
        self.total_log = str()
        self.seperate = f"{'-'*50}\r\n"
        self.sfis_seperate = f"{'SFIS':-^50}\r\n"
        self.iplas_separate = f"{'IPLAS':-^50}\r\n"
        
    def __repr__(self):
        self.total_log += f"{Log_Title(self.threal_local, self.thread_global)}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{DrawStringLogWithChinese(self.threal_local)}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{self.threal_local.log}\r\n"
        self.total_log += self.sfis_seperate
        self.total_log += f"{self.threal_local.sfis_log}\r\n"
        self.total_log += self.iplas_separate
        self.total_log += f"{self.threal_local.iplas_log}\r\n"

        return self.total_log


def generate_log(threal_local, thread_global):

    f = SingleTon_Global()
    
    if_sfif = 'On SFIS' if f.upload_func_open else 'Off SFIS'
    now_day = datetime.now().strftime("%m/%d")

    if threal_local.dut_info.get('SN'):
        log_path = f"{log_root_path}\Gemini\Burn_in\{if_sfif}\{now_day}"
        if not threal_local.dut_test_fail:
            log_name = f"{threal_local.dut_info['SN']}_[{threal_local.device_id}]_BURNIN_{thread_global.run_times}_{threal_local.VERSION}_[PASS]"
        else:
            log_name = f"{threal_local.dut_info['SN']}_[{threal_local.device_id}]_BURNIN_{thread_global.run_times}_{threal_local.VERSION}_[FAIL][{threal_local.error_code}]"
    
    else:
        log_name = f"{thread_global.telnet_port}_[{thread_global.device_id}]_BURNIN_{thread_global.run_times}_{threal_local.VERSION}_[FAIL][{threal_local.error_code}]"

    os.makedirs(log_path, exist_ok=True) 

    file_repeat_num = 0
    while True:
        final_path = os.path.join(log_path, f"{log_name}.txt")
        if os.path.isfile(final_path):
            file_repeat_num += 1
            log_name = f"{log_name}_{file_repeat_num}.txt"
        else:
            break
    
    with open(final_path, 'w+', newline='', encoding="utf-8") as f:
        f.write(Gearate_log(threal_local, thread_global))
    
    ftp_path = "/".join(log_path.split('\\')[len(log_root_path.split('\\')):-1])

    threal_local.ftp_local_path = final_path
    threal_local.ftp_remote_path = ftp_path
    return threal_local, thread_global



    













