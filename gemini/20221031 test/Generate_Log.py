import os 
from datetime import datetime
import threading
from Global_Variable import SingleTon_Global
from Log_Dealer import Upload_Log_Tranfer
import shutil

log_root_path = r'.\log'


class DrawStringLogWithChinese():

    G = SingleTon_Global()

    def __init__(self):
        """
        畫圖表(可使用中文字體)，回傳String
        """
        self.l = self.p[threading.get_ident()]
        self.raw_data_list = self.l['_form_log']

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

    def __str__(self):
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
    
    G = SingleTon_Global()

    def __init__(self):
        """
        傳回log title的資料
        """
        self.l = self.p[threading.get_ident()]
        self._title_data = {'program_version' : self.G.VERSION, 
                    'test_result' : "PASS" if not self.l['_dut_test_fail'] else "FAIL",
                    'error_code' : self.l['_dut_error_code'],
                    'csn' : self.l['_dut_info'].get('SN'),
                    'start_time' : self.l['_test_start_time'],
                    'end_time' : self.l['_test_end_time']}
        

    def __str__(self):
        temp_str = str()
        for name, data in self._title_data.items():
            temp_str += f"{name} : {data}\r\n"
        return temp_str.strip()


class Gearate_log():


    def __init__(self):
        self.l = self.p[threading.get_ident()]
        self.total_log = str()
        self.seperate = f"{'-'*50}\r\n"
        self.sfis_seperate = f"{'SFIS':-^50}\r\n"
        self.iplas_separate = f"{'IPLAS':-^50}\r\n"
        
    def __str__(self):
        self.total_log += f"{Log_Title()}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{DrawStringLogWithChinese()}\r\n"
        self.total_log += self.seperate
        self.total_log += f"{self.l['_log']}\r\n"
        self.total_log += self.sfis_seperate
        self.total_log += f"{self.l['_sfis_log']}\r\n"
        self.total_log += self.iplas_separate
        self.total_log += f"{self.l['_iplas_log']}\r\n"

        return self.total_log


def transfer_log(l):
    G = SingleTon_Global()
    l['_log'] += G.log_model(l['_log_raw_data'])
    l['_sfis_log'] += Upload_Log_Tranfer.transfer_to_sfis(l['_upload_data'])
    l['_iplas_log'] += Upload_Log_Tranfer.transfer_to_iplas(l['_upload_data'])
    l['_form_log'] += Upload_Log_Tranfer.transfer_to_form(l['_upload_data'])


def generate_log():
    l = p[threading.get_ident()]
    G = SingleTon_Global()
    transfer_log(l)

    if_sfif = 'On SFIS' if G.online_function else 'Off SFIS'
    now_day = datetime.now().strftime("%m/%d")

    if l['_dut_info'].get('SN'):
        log_path = fr"{G.log_root_path}\Gemini\Burn in\{if_sfif}\{now_day}"
        if not l['_dut_test_fail']:
            log_name = fr"{l['_dut_info'].get('SN')}_[{l['device_id']}]_BURNIN_{l['run_times']}_{G.VERSION}_[PASS]"
        else:
            log_name = fr"{l['_dut_info'].get('SN')}_[{l['device_id']}]_BURNIN_{l['run_times']}_{G.VERSION}_[FAIL][{l['_dut_error_code']}]"
    
    else:
        log_path = fr"{G.log_root_path}\Gemini\Burn in\{if_sfif}\{now_day}\unsort log"
        log_name = fr"{l['telnet_port']}_[{l['device_id']}]_BURNIN_{l['run_times']}_{G.VERSION}_[FAIL][{l['_dut_error_code']}]"

    os.makedirs(log_path, exist_ok=True)

    file_repeat_num = 0
    new_name = f"{log_name}.txt"
    while True:
        final_path = os.path.join(log_path, new_name)
        if os.path.isfile(final_path):
            file_repeat_num += 1
            new_name = f"{log_name}_{file_repeat_num}.txt"
        else:
            break
    
    with open(final_path, 'w+', newline='', encoding="utf-8") as f:
        f.write(str(Gearate_log()))
    
    ftp_path = "/".join(log_path.split('\\')[len(log_root_path.split('\\')):-1])
    ftp_path = f"{G.ftp_upload_path}/{ftp_path}"


    iplas_log_path = fr"{log_path}\iplas"
    os.makedirs(iplas_log_path, exist_ok=True)
    iplas_log_name = f"{log_name}_iplas"
    iplas_log_path = os.path.join(iplas_log_path, f"{iplas_log_name}.txt")
    shutil.copyfile(final_path, iplas_log_path)


    l['_ftp_local_path'] = final_path
    l['_ftp_remote_path'] = ftp_path
    l['_iplas_log_path'] = iplas_log_path




    













