import sys
import os
import traceback
import time
from enum import Enum
from PySide6.QtCore import Qt
from LSF_DataTransfer import DataTransfer
from LSF_ToExcel import Transfer_Excel
from LSF_ToPDF import Transfer_PDF, PDF_Merge

root_path = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT'
data = {'input_X_shear':rf'{root_path}\VPDATXE_NSW.txt',
        'input_X':rf'{root_path}\VPDATXE.txt',
        'input_Y_shear':rf'{root_path}\VPDATYE_NSW.txt',
        'input_Y':rf'{root_path}\VPDATYE.txt',
        'adjust':False,
        }
#'level':'1MF',
#'H':5.45,
# excel_output_path = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT\report.xlsx'
# pdf_output_file = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT'
# final_pdf = r'C:\Users\andy_chien\Downloads\資料\REPORT.pdf'

ui_signal = None

class Text_Color(Enum):
    black = Qt.black
    darkYellow = Qt.darkYellow
    red = Qt.red
    blue = Qt.blue
    darkGreen = Qt.darkGreen

class UI_Signal():
    def __init__(self, ui_signal=None):
        self.ui_signal = ui_signal

    def Show_Status(self, txt, color=Text_Color.black.value):
        if self.ui_signal:
            self.ui_signal.status.emit((txt, color))
    
    def MSG_Exception(self, data:str):
        if self.ui_signal:
            self.ui_signal.exception.emit(data)
    
    def Finished(self):
        if self.ui_signal:
            self.ui_signal.finish.emit()

    def FinalPath(self, path:str):
        if self.ui_signal:
            self.ui_signal.final_path.emit(path)
        

def debug(func):
    def warpper(*args, **wargs):
        try:
            final_pdf_path = func(*args, **wargs)
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
            ui_signal.MSG_Exception(f'Error: {errMsg}')
        else:
            ui_signal.Finished()
            ui_signal.FinalPath(final_pdf_path)

    return warpper

@debug
def Main(data:dict, signals=None):
    global ui_signal
    ui_signal = UI_Signal(signals)

    pdf_list = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "弱層說明頁.pdf")]

    excel_output_path, final_pdf_path = get_output_path(data['input_path'])
    X_shear_data, Y_shear_data = DataTransfer(data)
    Transfer_Excel(X_shear_data, Y_shear_data, excel_output_path)
    pdf_list = Transfer_PDF(pdf_list, excel_output_path, data['input_path'])
    PDF_Merge(pdf_list, final_pdf_path)
    return final_pdf_path



def get_output_path(input_path):
    excel_output_path = os.path.join(input_path, "report.xlsx")
    final_pdf_path = os.path.join(input_path, "REPORT.pdf")
    return excel_output_path, final_pdf_path





if __name__ == "__main__":
    Main(data)