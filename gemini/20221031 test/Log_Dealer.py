from functools import partial
from enum import Enum
from datetime import datetime


class _log_dealer():

    @staticmethod
    def _no_name_time(data:dict):
        """
        不顯示測項名稱與時間
        """
        tmp_log = str()
        for test_name, test_data in data.items():
            tmp_log += test_data['log']
        return tmp_log
        
    @staticmethod
    def _name(data:dict):
        """
        只測項名稱
        """
        tmp_log = str()
        for test_name, test_data in data.items():
            temp_title = f"{test_name:-^60}\n"
            tmp_log += f"{temp_title}{test_data['log'].strip()}\n"
        return tmp_log

    @staticmethod
    def _name_time(data:dict):
        """
        顯示測項名稱與時間
        """
        tmp_log = str()
        for test_name, test_data in data.items():
            start_time = test_data['start_time'].strftime("%H:%M:%S")
            end_time = test_data['end_time'].strftime("%H:%M:%S")
            temp = f"{test_name} {start_time}"
            start_title = f"{temp:-^60}\n"
            end_title = f"{end_time:-^60}\n"
            tmp_log += f"{start_title}{test_data['log'].strip()}\n{end_title}"
        return tmp_log


class Log_Model(Enum):
    no_name_no_time = partial(_log_dealer._no_name_time)
    only_name = partial(_log_dealer._name)
    name_time = partial(_log_dealer._name_time)

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)



class Upload_Log_Tranfer():

    @staticmethod
    def transfer_to_sfis(data:dict):
        temp_log = str()
        for test_item_name, test_data in data.items(): 
            temp_log += test_item_name
            for i, vlaue in enumerate(test_data[:-1]):
                if vlaue == None and i == 1:
                    temp_log += f",PASS" if test_data[0] == 1 else ",FAIL"
                if vlaue != None:
                    temp_log += f",{vlaue}"
            temp_log += '\r\n'

        return temp_log.strip()

    @staticmethod
    def transfer_to_sfis_raw_data(upload_log, G):
        title = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{G.VERSION}\r\n'
        title += Upload_Log_Tranfer.transfer_to_sfis(upload_log)
        return title


    @staticmethod
    def transfer_to_iplas(data:dict):
        temp_log = str()
        for test_item_name, test_data in data.items():
            temp_log += test_item_name
            temp_log += ',PASS' if test_data[0] else ',FAIL'
            temp_log += ',PASS' if test_data[1] == None else f",{test_data[1]}"
            temp_log += ',' if test_data[2] == None else f",{test_data[2]}"
            temp_log += ',' if test_data[3] == None else f",{test_data[3]}"
            temp_log += ',' if test_data[5] == None else f",{test_data[5]}" 
            temp_log += '\r\n'

        return temp_log.strip()

    @staticmethod
    def transfer_to_iplas_raw_data(l, G):
        project = 'Gemini'
        model = ''
        test_result = 'PASS' if not l.dut_test_fail else 'FAIL'
        error_code = l.error_code if len(l.error_code) else ''
        send_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        title = "TEST,STATUS,VALUE,UCL,LCL,CYCLE\r\n"
        title += f"ISN,,{l.dut_sfis_sn},,,0\r\n"
        title += f"Project,,{project},,,0\r\n"
        title += f"TSP,,BURNIN,,,0\r\n"
        title += f"Type,,ONLINE,,,0\r\n"
        title += f"Test Start Time,,{l.test_start_time},,,0\r\n"
        title += f"Test end Time,,{l.test_end_time},,,0\r\n"
        title += f"DeviceId,,{l.device_id},,,0\r\n"
        title += f"Model,,{model},,,0\r\n"
        title += f"Line,,61F53D12,,,0\r\n"
        title += f"Slot,,,,,0\r\n"
        title += f"MO,,,,,,0\r\n"
        title += f"SN,,{l.dut_sfis_sn},,,0\r\n"
        title += f"CVP_Ver,,Pegatron_{G.VERSION},,,0\r\n"
        title += f"ProducerVersion,,2.0.0.0,,,0\r\n"
        title += f"Build,,,,,0\r\n"
        title += f"Test Status,,{test_result},,,0\r\n"
        title += f"ErrorCode,,{error_code},,,0\r\n"
        title += f"CONFIG,,,,,0\r\n"
        title += f"CallerSendTime,,{send_time},,,0\r\n"         

        title += Upload_Log_Tranfer.transfer_to_iplas(l.upload_log)
        return title

    @staticmethod
    def transfer_to_form(data:dict):
        temp_list = list()
        
        for test_item_name, test_data in data.items():
            temp_log = list()
            temp_log.append(test_item_name)
            temp_log.append('PASS' if test_data[0] else 'FAIL')
            for i, vlaue in enumerate(test_data[1:]):
                if vlaue == None:
                    temp_log.append('')
                else:
                    temp_log.append(str(vlaue))
            temp_list.append(temp_log)
        return temp_list

    @staticmethod
    def transfer_to_form_raw_data(upload_log):
        title = [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time (s)>']]
        title.extend(Upload_Log_Tranfer.transfer_to_form(upload_log))
        return title
            


if "__main__" == __name__:
    upload_log= {'Check_Telnet_Connect': (1, None, None, None, None, 0), 'Boot_Up': (0, None, None, None, 'B00OT000002', 21)}
    j = Upload_Log_Tranfer()
    title = [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time (s)>']]
    tmp = j.transfer_to_form(upload_log)
    title.extend(tmp)
    
    print(title)