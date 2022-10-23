from functools import partial
from enum import Enum


class _log_dealer():

    @staticmethod
    def _no_name_time(data:dict):
        """
        不顯示測項名稱與時間
        """
        for test_name, test_data in data.items():
            return test_data[1]
        
    @staticmethod
    def _name(data:dict):
        """
        只測項名稱
        """
        for test_name, test_data in data.items():
            temp_title = f"{test_name:-^60}\n"
            return f"{temp_title}{test_data[1].strip()}\n"

    @staticmethod
    def _name_time(data:dict):
        """
        顯示測項名稱與時間
        """
        for test_name, test_data in data.items():
            start_time = test_data[0].strftime("%H:%M:%S")
            end_time = test_data[2].strftime("%H:%M:%S")
            temp = f"{test_name} {start_time}"
            start_title = f"{temp:-^60}\n"
            end_title = f"{end_time:-^60}\n"
            return f"{start_title}{test_data[1].strip()}\n{end_title}"


class Log_Model(Enum):
    no_name_time = partial(_log_dealer._no_name_time)
    name = partial(_log_dealer._no_name_time)
    name_time = partial(_log_dealer._name_time)


class Upload_Log_Tranfer():

    @staticmethod
    def to_sfis(data:dict):
        pass

    def to_iplas(data:dict):
        pass