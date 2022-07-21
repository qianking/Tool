from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from glob import glob
from copy import deepcopy

path = r'D:\download\整合PDF\整合前\test_1.pdf'
outputFile = r'C:\Users\andy_chien\Downloads\整合PDF\Test_2.pdf'
path_home=r'D:\download\整合PDF\整合前\02_V534_(111.04.13)_地震風力整合大全(100年)_110.12.31_Locked.pdf'



folder = r'C:\Users\andy_chien\Downloads\整合PDF\整合前'
file_list = glob(f"{folder}\*.pdf")
#print(file_list)


class Add_Page_Number():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
    
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
                    with open(outputFile, 'wb') as f:
                        output.write(f)
            os.remove(tmp_pdf)


class Merge_Pdf_and_GetOutline():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_list = glob(f"{self.folder_path}\*.pdf")
        self.order_dic = {}
        self.order_list = []
        self.title = {'設計概要說明':1, '軟層之檢核':3, '牆之剪力設計':3, '一樓板剪力傳遞':3, '梁上柱檢核':3, '梁柱韌性':3, '極限層剪力':3, '上浮力檢核':3, '地下室外牆設計':3, '無梁版':3, '基礎設計':3}
        self.title_1 = ('設計概要說明', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心', 
                            '2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析', '2.5．動力分析', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算')
        #self.title_key_word = ('設計概要說明', '軟層之檢核', '牆之剪力設計', '一樓板剪力傳遞', '梁上柱檢核', '梁柱韌性', '極限層剪力', '上浮力檢核', '地下室外牆設計', '無梁版', '基礎設計')        
        self.title_all = ('設計概要說明','軟層檢核', '剪力牆設計', '一樓樓版剪力傳遞', '梁上柱檢核', '梁柱韌性與扭力檢核', '極限層剪力檢核', '上浮力檢核', '地下室外牆設計', '無梁版檢核', '基礎設計')
        
        self.outline = {'一、結構資料': [], 
                        '二、地震力與風力計算': [], 
                        '三、結構設計檢核': []}

    def merge_pdf(self):
        pages = 1
        last_key = 0
        num = 0
        merger = PdfMerger(strict = False)
        for key, values in self.order_dic.items():
            
            PdfReader = PdfFileReader(values[0])
            merger.append(values[0])

            pages, last_key, num = self.get_outline(key, values, PdfReader, pages, last_key, num)

        merger.write(outputFile)
        merger.close()
            

    def get_outline(self, key, values, PdfReader, pages, last_key, num):
        if key == 0:                                              #前一、二大標題
            last_key = 0
            pages = 1
            self.title_1_list = list(deepcopy(self.title_1))           
            for page in range(PdfReader.getNumPages()):
                if len(self.title_1_list) != 0:
                    title = self.title_1_list[0]
                Page_n = PdfReader.getPage(page)
                txt = Page_n.extractText()
                if title in txt:
                    title_index = self.title_1.index(title)
                    if title_index < 5:
                        title = title.replace('．', ' ')
                        tmp = (title, page+1)
                        self.outline['一、結構資料'].append(deepcopy(tmp))
                    elif 4 < title_index < 15:
                        title = title.replace('．', ' ')
                        tmp = (title, page+1)
                        self.outline['二、地震力與風力計算'].append(deepcopy(tmp))

                    self.title_1_list.pop(0)
                    del tmp
        elif 0 < key:                                                #第三大標題
            num += 1
            pages = pages + self.order_dic[last_key][2]
            tmp = (f'{num}. {values[1]}', pages + 1)
            self.outline['三、結構設計檢核'].append(deepcopy(tmp))

            if key == 10:
                num = 0

            del tmp
        last_key = key
        return pages, last_key, num

    
    

    
    """ def order_pdf_file(self):
        for pdf in file_list:
            with open(pdf, 'rb') as pdfFileObj: 
                PdfReader = PdfFileReader(pdfFileObj)
                Page_1 = PdfReader.getPage(0)
                txt = Page_1.extractText()
                txt = txt.split('\n')[0:2]          #取前三行
                txt = ' + '.join(txt)
                for title in self.title_key_word:
                    if title in txt:
                        index_title = self.title_key_word.index(title)
                        self.order_dic[index_title] = [pdf, self.title_all[index_title], PdfReader.getNumPages()] 
                        
        self.order_dic = dict(sorted(self.order_dic.items())) """
        



if "__main__" == __name__:
    #print(u"\u0121")
    pdf =  Merge_Pdf_and_GetOutline(folder)
    pdf.order_pdf_file()
    pdf.merge_pdf()
    print(pdf.order_dic)
    print(pdf.outline)
    
