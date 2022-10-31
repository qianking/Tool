import sys
import traceback


class TimeOutError(Exception):
    pass

class TestItemFail(Exception):
    """
    填入 
    測項名稱, 如果跟測試項目名稱一樣就填None
    測項參數(值, 下限, 上限)(如果沒有就填None), 
    """
    pass
            

class Test_Fail(Exception):
    pass

class Online_Fail(Exception):
    pass



def error_dealer(ex):
    error_class = ex.__class__.__name__ #取得錯誤類型
    detail = ex.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2]#取得發生的函數名稱
    errMsg = f"{[error_class]}\n\"{fileName}\", line {lineNum}, in {funcName}\n{detail}"
    return errMsg



       
        


