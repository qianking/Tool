from reportlab.pdfgen import canvas
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from glob import glob
from copy import deepcopy
import re
import datetime
import write_word_pdf as word_pdf

"""
如果要使用本檔案，需先去 python\lib\site-packages\PyPDF2\_camp.py 檔案中的第287行 註解掉這行
"""

All_chapter = \
{1:'結構資料',
2:'地震力與風力計算',
3:'結構設計檢核',
4:'開挖設計',    #開挖設計這章沒小章節，所以頁數不用+1
5:'結構外審意見回覆',
6:'設計分析報表'
}
All_file_name = \
{1:['結構資料'],
3: ['軟層檢核', '剪力牆設計', '一樓樓版剪力傳遞', '梁上柱檢核', '梁柱韌性與扭力檢核', '極限層剪力檢核', '上浮力檢核', '地下室外牆設計', '無梁版檢核', '基礎設計'],
4: ['開挖設計'],
5: ['第一次意見回覆','第二次意見回覆', '第三次意見回覆', '會後意見回覆'],
6: ['大梁、柱、牆', '小梁、版']}

Chapter_1_inner_title = \
{1:['1-1~1-10．設計概要說明', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心'],
2: ['2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算']}

Chapter_number = \
{1: '一',
2:'二',
3:'三',
4:'四',
5:'五',
6:'六'}

class Merge_Pdf_and_GetOutline():
    def __init__(self, input_pdf_folder_path, output_path):
        self.input_pdf_folder_path = input_pdf_folder_path
        self.output_path = output_path
        self.file_list = glob(f"{self.input_pdf_folder_path}\*.pdf")

    def order_file(self):
        order_dic = {1:{1:{'結構資料':[]}}, 3:{}, 4:{}, 5:{}, 6:{}}
        self.debug_file_list = deepcopy(self.file_list)
        for pdf in self.file_list:
            pdf_name = pdf.split('\\')[-1]
            order_dic = self.find_file_chapter(order_dic, pdf_name)
        
        self.sort_order_dic(order_dic)

        #print(order_dic)
        self.final_order_file = self.re_order_chapter_number(order_dic)
        print(self.final_order_file)

    @staticmethod
    def find_file_chapter(order_dic, pdf_name):
        tmp_dic = {}
        for chapter, file_name_list in All_file_name.items():
            for name in file_name_list:
                if name in pdf_name:
                    if chapter == 1:
                        order_dic[1][1]['結構資料'].append(pdf_name)
                    else:
                        order_dic[chapter][0] = deepcopy(All_chapter[chapter])
                        index = file_name_list.index(name)
                        tmp_dic[name] = pdf_name
                        order_dic[chapter][index+1] = deepcopy(tmp_dic)
                        tmp_dic.clear()
        return order_dic
    
    @staticmethod
    def sort_order_dic(order_dic):
        for num in list(order_dic.keys()):
            if len(order_dic[num]) == 0:
                order_dic.pop(num)
                continue
            order_dic[num] = dict(sorted(order_dic[num].items()))
    
    @staticmethod
    def re_order_chapter_number(order_dic):
        start_num = 3
        tmp_dic = {}
        chapter_1 = order_dic.pop(1)
        tmp_dic[1] = chapter_1
        for chapter in list(order_dic.keys()):
            chapter_n = order_dic.pop(chapter)
            tmp_dic[start_num] = chapter_n
            start_num += 1
        return tmp_dic
    
    def generate_cover_pdf(self):
        tmp_dic = {}
        chapter_list = list(self.final_order_file.keys())
        for chpater in chapter_list[1:]:
            chapter_name = self.final_order_file[chpater][0]
            chapter_num = Chapter_number[chpater]
            tmp_dic['chapter'] = chapter_num
            tmp_dic['title'] = chapter_name
            doc_output_path = word_pdf.write_cover_word(self.output_path, f'cover_{chpater}', tmp_dic)
            pdf_output_path = word_pdf.turn_word_to_pdf(doc_output_path)
            self.final_order_file[chpater][0] = {chapter_name : pdf_output_path}
    

    def one_build_set(self):
        
        


        

             
    
        



if "__main__" == __name__:
    pdf = Merge_Pdf_and_GetOutline(r'E:\python\github\Tool\pdf_merge\整合PDF(all)\整合前', r'E:\python\github\Tool\pdf_merge\整合PDF(all)\整合前')
    pdf.order_file()
    pdf.generate_cover_pdf()
    print(pdf.final_order_file)


