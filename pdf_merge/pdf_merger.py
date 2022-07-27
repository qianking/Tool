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

class Add_Page_Number():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
    
    def get_output_path(self):
        now_date = datetime.date.today()
        path = self.pdf_path.split('\\')[:-1]
        path = '\\'.join(path)
        name = f"{now_date}_page_number.pdf"
        file_path = os.path.join(path, name)
        return file_path

    
    def get_page_size(self, origin_pdf, page_numbers):
        """
        得到一個包含每頁PDF寬度/2(中間點)位置的list
        """
        page_middle_position = []

        for i in range(page_numbers):
            width = float(origin_pdf.pages[i].mediabox.getWidth())
            page_middle_position.append(width/2)
        
        print(page_middle_position)
        return page_middle_position
    
    def create_page_pdf(self, page_numbers, tmp_pdf, page_middle_position):
        """
        創建一個只有頁數在位於中下地方的PDF檔案
        """
        c = canvas.Canvas(tmp_pdf)
        for i in range(1, page_numbers+1):
            c.drawString((page_middle_position[i-1]), 20, str(i))
            #c.setFont()
            c.showPage()
        c.save()

    def add_page_numbers(self):
        tmp_pdf = "__tmp.pdf"           #用來畫頁數的PDF檔案 

        output = PdfFileWriter()      
        with open(self.pdf_path, 'rb') as f:      
            origin_pdf = PdfFileReader(f, strict = False)   
            page_numbers = origin_pdf.getNumPages()

            page_middle_position = self.get_page_size(origin_pdf, page_numbers)
            self.create_page_pdf(page_numbers, tmp_pdf, page_middle_position)

            with open(tmp_pdf, 'rb') as ftmp:
                numberPDF = PdfFileReader(ftmp)
                for p in range(page_numbers):
                    page = origin_pdf.getPage(p)
                    numberLayer = numberPDF.getPage(p)

                    page.mergePage(numberLayer)
                    output.addPage(page)

                if output.getNumPages():
                    path = self.get_output_path()
                    with open(path, 'wb') as f:
                        output.write(f)
            os.remove(tmp_pdf)


class Merge_Pdf_and_GetOutline():
    def __init__(self, folder_path, output_path):
        self.folder_path = folder_path
        self.output_path = output_path
        self.file_list = glob(f"{self.folder_path}\*.pdf")
        self.insert_page = {1:None,
                            2:None,
                            3:'.\\cover\\第三章封面.pdf',
                            4:'.\\cover\\第四章封面.pdf',
                            5:'.\\cover\\第五章封面.pdf',
                            6:'.\\cover\\第六章封面.pdf'}
        self.order_dic = {1:{0:['結構資料', None]}, 2:{0:['地震力與風力計算',None]}, 3:{0:['結構設計檢核', self.insert_page[3]]}, 4:{0:['開挖設計', self.insert_page[4]]}, 5:{0:['結構外審意見回覆', self.insert_page[5]]}, 6:{0:['設計分析報表', self.insert_page[6]]}}
        self.title = {1:['結構資料', '1-1~1-10．設計概要說明', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心'],
                    2:['地震力與風力計算', '2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算'], 
                    3:['結構設計檢核', '軟層檢核', '剪力牆設計', '一樓樓版剪力傳遞', '梁上柱檢核', '梁柱韌性與扭力檢核', '極限層剪力檢核', '上浮力檢核', '地下室外牆設計', '無梁版檢核', '基礎設計'],
                    4:['開挖設計'],
                    5:['結構外審意見回覆', '意見回覆'],
                    6:['設計分析報表','大梁', '小梁']}
        
        
        self.outline = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}
        self.to_word_outline = {}

        self.debug_file_list = []
        self.debug_title_list = []


    def get_output_file_path(self):
        now_date = datetime.date.today()
        file_name = f'{now_date}_merge.pdf'
        self.output_merge_pdf_path = os.path.join(self.output_path, file_name)


    def merge_and_getpage(self):
        page = 0
        merger = PdfMerger()
        for key, values in self.order_dic.items():
            for num, pdf_path in values.items():
                if num == 0:                                    #num == 0時為插入大標題的封面頁，所以頁數+1
                    if pdf_path[1]:
                        merger.append(pdf_path[1])
                        page += 1
                        self.outline[key][pdf_path[0]] = page
                else:
                    title_name = pdf_path[0]
                    PdfReader = PdfFileReader(pdf_path[1])
                    page = self.get_outline_page(key, title_name, page, PdfReader)
                    merger.append(pdf_path[1])

        self.get_output_file_path()
        merger.write(self.output_merge_pdf_path)
        merger.close()
        
    def order_file(self):
        patern = r'(\d\d)_(\d\d)'
        self.debug_file_list = deepcopy(self.file_list)
        for pdf in self.file_list:
            file_name = pdf.split('\\')[-1]
            num_list = re.findall(patern, file_name)
            chapter = int(num_list[0][0])
            if chapter == 2:                                       #第一大章節的資料一律存在self.order_dic[1]，不論他前面標的數字為01還是02
                chapter = 1
            num = int(num_list[0][1])
            for title_name in self.title[chapter]:
                if title_name in file_name:
                    self.order_dic[chapter][num] =[title_name, pdf] 
                    index = self.debug_file_list.index(pdf)
                    self.debug_file_list.pop(index)                          #找到符合的pdf就pop出來，直到找完
            
            
        for i in list(self.order_dic.keys()):
            self.order_dic[i] = dict(sorted(self.order_dic[i].items()))
        

    
    def get_outline_page(self, key, title_name, page, PdfReader):
        if key == 1:
            self.title_1_2_list = list(deepcopy(self.title[1][1:]))
            self.title_1_2_list.extend(list(deepcopy(self.title[2][1:])))
            self.debug_title_list = deepcopy(self.title_1_2_list)
            self.outline[1][self.title[1][0]] = None
            self.outline[2][self.title[2][0]] = None 
            _page = PdfReader.getNumPages()

            for pages in range(_page):                       
                Page_n = PdfReader.getPage(pages)
                txt = Page_n.extractText()
                if len(self.debug_title_list) != 0:
                    title = self.debug_title_list[0]
                    pure_title = title.split('．')[1]
                    try:
                        title_num = int(title.split('-')[0])
                    except:
                        title_num = int(title.split('.')[0])
                    if pure_title in txt:
                        title_change = title.replace('．', ' ')
                        self.outline[title_num][title_change] = pages + 1
                        self.debug_title_list.pop(0)                   
         
        elif key >= 3:
            _page = PdfReader.getNumPages()
            if key == 4:
                self.outline[key][title_name] = page              #如果只有大標題沒小標題的話就不用+1
            else:
                self.outline[key][title_name] = page + 1          #如果有大標題且有小標題的話小標題頁數要從大標題封面那頁+1

        page += _page
        return page

    def transfer_outline(self):
        for chapter, data in self.outline.items():
            tmp_list = []
            title_list = list(data.keys())
            for title in title_list:
                if data[title_list[0]]:
                    self.to_word_outline[f'cover_{chapter}'] = deepcopy(data[title_list[0]])
                for tit in title_list[1:]:
                    tmp_dic = {}
                    tmp_dic['title'] = deepcopy(tit)
                    tmp_dic['page'] = deepcopy(data[tit])
                    tmp_list.append(deepcopy(tmp_dic))
                    tmp_dic.clear()
                self.to_word_outline[f'title_{chapter}'] = deepcopy(tmp_list)
                del tmp_list[:]


def Merge_Final_PDF(first_page_pdf_path, output_merge_pdf_path, number, final_file_name):
    tmp_final_pdf_path = first_page_pdf_path.split('\\')[:-1]
    final_pdf_path = '\\'.join(tmp_final_pdf_path)
    if final_file_name:
        final_pdf_name = final_file_name
    else:
        final_pdf_name = f'{number}_結構計算書(全).pdf'
    final_path = os.path.join(final_pdf_path, final_pdf_name)
    merger = PdfMerger(strict = False)
    merger.append(first_page_pdf_path)
    merger.append(output_merge_pdf_path)
    merger.write(final_path)
    merger.close()
    return final_path






        

        
    



            


if "__main__" == __name__:
    #print(u"\u0121")
    check_folder_file('C:\\Users\\andy_chien\\Downloads\\整合PDF(all)\\整合前')
    
    
    
