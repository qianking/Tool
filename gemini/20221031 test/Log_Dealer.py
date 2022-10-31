from functools import partial
from enum import Enum


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
    def transfer_to_iplas(data:dict):
        temp_log = str()
        for test_item_name, test_data in data.items():
            temp_log += test_item_name
            temp_log += ',PASS' if test_data[0] else ',FAIL'
            for i, vlaue in enumerate(test_data[1:]):
                if vlaue == None and i == 1:
                    temp_log += f",PASS" if test_data[0] == 1 else ",FAIL"
                if vlaue != None:
                    temp_log += f",{vlaue}"
            temp_log += '\r\n'

        return temp_log.strip()

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
            


if "__main__" == __name__:
    upload_log= {'Check_Telnet_Connect': (1, None, None, None, None, 0), 'Boot_Up': (1, None, None, None, None, 100), 'Get_SN': (1, None, None, None, None, 3), 'Rebbot': (1, None, None, None, None, 14)}
    j = Upload_Log_Tranfer()
    print(j.transfer_to_form(upload_log))