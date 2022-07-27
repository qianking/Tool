from reportlab.pdfgen import canvas
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from glob import glob
from copy import deepcopy
import re
import datetime

"""
如果要使用本檔案，需先去 python\lib\site-packages\PyPDF2\_camp.py 檔案中的第287行 註解掉這行
"""
All_title = \
{1:['結構資料', '1-1~1-10．設計概要說明', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心'],
2: ['地震力與風力計算', '2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算'],
3: ['結構設計檢核', '軟層檢核', '剪力牆設計', '一樓樓版剪力傳遞', '梁上柱檢核', '梁柱韌性與扭力檢核', '極限層剪力檢核', '上浮力檢核', '地下室外牆設計', '無梁版檢核', '基礎設計'],
4: ['開挖設計'],
5: ['結構外審意見回覆', '第一次意見回覆','第二次意見回覆', '第三次意見回覆', '會後意見回覆'],
6: ['設計分析報表','大梁、柱、牆', '小梁、版']}


class Merge_Pdf_and_GetOutline():
    def __init__(self, folder_path, output_path):
        self.input_pdf_folder_path = folder_path
        self.output_path = output_path
        self.file_list = glob(f"{self.input_pdf_folder_path}\*.pdf")