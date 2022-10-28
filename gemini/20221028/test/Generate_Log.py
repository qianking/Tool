import os 
from datetime import datetime
from copy import deepcopy
from Global_Variable import SingleTon_Variable, SingleTon_Global

log_root_path = r'.\log'

class DrawStringLogWithChinese():
    
    v = SingleTon_Variable()

    def __init__(self):
        """
        畫圖表(可使用中文字體)，回傳String
        """
        self.raw_data_list = self.v.form_log

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
    
    v = SingleTon_Variable()

    def __init__(self):
        """
        傳回log title的資料
        """
        self._title_data = {'program_version' : self.v.VERSION, 
                    'test_result' : "PASS" if not self.v.dut_test_fail else "FAIL",
                    'error_code' : self.v.error_code,
                    'csn' : self.v.dut_info.get('SN'),
                    'start_time' : self.v.test_start_time,
                    'end_time' : self.v.test_end_time}
        

    def __repr__(self):
        temp_str = str()
        for name, data in self._title_data.items():
            temp_str += f"{name} : {data}\r\n"
        return temp_str.strip()


class Gearate_log():

    v = SingleTon_Variable()

    def __init__(self):
        self.total_log = str()
        self.seperate = f"{'-'*50}\r\n"
        self.sfis_seperate = f"{'SFIS':-^50}\r\n"
        self.iplas_separate = f"{'IPLAS':-^50}\r\n"
        
    def __repr__(self):
        self.total_log += f"{Log_Title()}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{DrawStringLogWithChinese()}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{self.v.log}\r\n"
        self.total_log += self.sfis_seperate
        self.total_log += f"{self.v.sfis_log}\r\n"
        self.total_log += self.iplas_separate
        self.total_log += f"{self.v.iplas_log}\r\n"

        return self.total_log


def generate_log():
    v = SingleTon_Variable()
    f = SingleTon_Global()
    
    if_sfif = 'On SFIS' if f.upload_func_open else 'Off SFIS'
    now_day = datetime.now().strftime("%m/%d")

    if v.dut_info.get('SN'):
        log_path = f"{log_root_path}\Gemini\Burn in\{if_sfif}\{now_day}"
        if not v.dut_test_fail:
            log_name = f"{v.dut_info['SN']}_[{v.device_id}]_BURNIN_{v.run_times}_{v.VERSION}_[PASS]"
        else:
            log_name = f"{v.dut_info['SN']}_[{v.device_id}]_BURNIN_{v.run_times}_{v.VERSION}_[FAIL][{v.error_code}]"
    
    else:
        log_path = f"{log_root_path}\Gemini\Burn in\{if_sfif}\{now_day}\unsort log"
        log_name = f"{v.telnet_port}_[{v.device_id}]_BURNIN_{v.run_times}_{v.VERSION}_[FAIL][{v.error_code}]"

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
        f.write(Gearate_log())
    
    ftp_path = "/".join(log_path.split('\\')[len(log_root_path.split('\\')):-1])

    v.ftp_local_path = final_path
    v.ftp_remote_path = ftp_path



    













