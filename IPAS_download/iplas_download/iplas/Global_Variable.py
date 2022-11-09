import traceback
import os, sys


class Send_to_UI():
    def __init__(self, signal = None):
        self.signal = signal

    def send_status(self, txt):
        if self.signal:
            self.signal.status.emit(txt)
    
    def send_error_box(self, txt):
        if self.signal:
            self.signal.error.emit(txt)
    
    def send_finish_signal(self):
        if self.signal:
            self.signal.finish.emit()


def get_exception_detail(ex):
    error_class = ex.__class__.__name__ #取得錯誤類型
    detail = ex.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastcallstack = traceback.extract_tb(tb)[1]#取得Call Stack的最後一筆資料
    print(lastcallstack)
    fileName = lastcallstack[0] #取得發生的檔案名稱
    lineNum = lastcallstack[1] #取得發生的行號
    funcName = lastcallstack[2] #取得發生的函數名稱
    error_txt = f"[ERROR TYPE] {error_class}\n[ERROR DETAIL] {detail}\n[ERROR PATH] in file \"{fileName}\", line {lineNum}, function [{funcName}]"
    print(error_txt)
    return error_txt



class _Global_Variable():
    docs_folder = str()
    user_data_path = fr"{docs_folder}/fw7ssv7b9bdb7ddn"
    user_password = list()
    logger = None
    ui_signal = Send_to_UI()
    chrome_driver_path = str()


class SingleTon_Variable(_Global_Variable):
    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 


