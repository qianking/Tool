from xml.dom import NotFoundErr
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

All_same_chapter = \
{1: {'title': '結構設計檢核', 'inner_title_and_file_name' : ['軟層檢核', '剪力牆設計', '一樓樓版剪力傳遞', '梁上柱檢核', '梁柱韌性與扭力檢核', '極限層剪力檢核', 'SRC梁檢核', 'SRC柱檢核', '上浮力檢核', '地下室外牆設計', '無梁版檢核', '基礎設計']},
2: {'title': '開挖設計', 'inner_title_and_file_name' : None}, #開挖設計這章沒小章節，所以頁數不用+1
3: {'title': '結構外審意見回覆', 'inner_title_and_file_name' : ['第一次意見回覆','第二次意見回覆', '第三次意見回覆', '會後意見回覆']},
4: {'title': '設計分析報表', 'inner_title_and_file_name' : ['大梁、柱、牆', '小梁、版']}}


#核章版
Stamp_ver_Chapter_1_2_data = \
{0: {'file_name': '結構資料'},
1:{'title': '結構設計概要說明', 'inner_title' : ['1-1．建築概要','1-2．結構系統', '1-3．結構模型示意圖', '1-4．設計規範', '1-5．主要材料強度', '1-6．設計載重', '1-7．構材尺寸', '1-8．分析程式', '1-9．載重組合', '1-10．地震作用時層間變位檢討', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心']},
2: {'title': '地震力與風力計算', 'inner_title' :['2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算']}}

#外審版
Audit_ver_Chapter_1_inner_title = \
{0: {'file_name': '外審意見回覆'}, 
1:{'title': '外審意見回覆', 'inner_title' :[f'附件_n']}}


Chapter_number = \
{1: '一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六'}

stytle = '核章版'

#stytle =['核章版': Stamp, '外審版': Audit]


class Merge_Pdf_and_GetOutline():
    def __init__(self, stytle, input_pdf_folder_path, output_path):
        self.stytle = stytle
        self.input_pdf_folder_path = input_pdf_folder_path
        self.output_path = output_path
        self.file_list = glob(f"{self.input_pdf_folder_path}\*.pdf")
        self.debug_file = deepcopy(self.file_list)
        self.special_chapter_file_path = ''
        self.same_chapter_flag = None
        self.delete_file_list = []
        self.all_chapter_dic = {}
        self.to_word_outline = {}
        

    def create_order_dic(self):
        self.same_chapter_dic = {}
        len_order = len(Chapter_number)
        for i in range(1, len_order+1):
            self.same_chapter_dic[i] = {}

        self.special_chapter_dic = {1:[]}


    def find_same_chapter_file(self):
        for pdf in self.file_list:
            pdf_file = self.find_the_same_chapter(pdf)
            if pdf_file:
                index = self.debug_file.index(pdf)
                self.debug_file.pop(index)
        
        if len(self.debug_file)!= 0:
            bug_file = '、'.join(self.debug_file)
            raise FileNotFoundError(f'WORNING! 有檔案未被合併 : {bug_file}，請檢查檔名!')

    def find_the_same_chapter(self, pdf):
        pdf_name = pdf.split('\\')[-1]
        for chapter, file_name_list in All_same_chapter.items():
            if file_name_list['inner_title_and_file_name']:
                for name in file_name_list['inner_title_and_file_name']:
                    if name in pdf_name:
                        name_index = file_name_list['inner_title_and_file_name'].index(name)
                        pdf_path = os.path.join(self.input_pdf_folder_path, pdf_name)
                        self.same_chapter_dic[chapter][name_index+1] = {'title': name, 'pdf_path': pdf_path}
                        self.same_chapter_dic[chapter][0] = {'title': file_name_list['title']}
                        return pdf
            else:
                name = file_name_list['title']
                if name in pdf_name:
                    pdf_path = os.path.join(self.input_pdf_folder_path, pdf_name)
                    self.same_chapter_dic[chapter][1] = {'title': None, 'pdf_path': pdf_path}
                    self.same_chapter_dic[chapter][0] = {'title': name}
                    return pdf

    def order_same_chpater(self):
        count_ch = 1
        for capter in range(1, len(self.same_chapter_dic)+1):
            title_count = 1
            count = 1
            tmp_dic = {}
            if len(self.same_chapter_dic[capter]) != 0:
                title_data = self.same_chapter_dic.pop(capter)
                tmp_data = title_data.pop(0)
                tmp_dic[0] = deepcopy(tmp_data)
                while len(title_data) != 0:
                    try:
                        tmp_data = title_data.pop(title_count)
                        tmp_title = tmp_data['title']
                        if tmp_title:
                            if len(str(count)) == 1:
                                tmp_title = f"{count}.  {tmp_title}"
                            elif len(str(count)) == 2:
                                tmp_title = f"{count}. {tmp_title}"
                            tmp_data['title'] = tmp_title
                        tmp_dic[count] = deepcopy(tmp_data)
                    except:
                        title_count += 1
                    else:
                        count += 1
                self.same_chapter_dic[count_ch] = deepcopy(tmp_dic)
                count_ch +=1
            else:
                self.same_chapter_dic.pop(capter)

    def find_special_chapter_file(self):
        flag = False
        if stytle == '核章版':
            for pdf in self.file_list:
                pdf_name = pdf.split('\\')[-1]
                if Stamp_ver_Chapter_1_2_data[0]['file_name'] in pdf_name:
                    index = self.debug_file.index(pdf)
                    self.debug_file.pop(index)
                    self.special_chapter_dic[1].append(pdf)
                    flag = True
                    break
            
            if not flag:
                raise FileNotFoundError('WORNING! 找不到核章版版第一章檔案!')
                  
        if stytle == '外審版':
            for pdf in self.file_list:
                pdf_name = pdf.split('\\')[-1]
                if Audit_ver_Chapter_1_inner_title[0]['file_name'] in pdf_name:
                    index = self.debug_file.index(pdf)
                    self.debug_file.pop(index)
                    self.special_chapter_dic[1].append(pdf)
                    flag = True
                    break

            if not flag:
                raise FileNotFoundError('WORNING! 找不到外審版第一章檔案!')
        
       
    def find_special_chapter_page(self):
        if stytle == '核章版':
            self.find_Stamp_page()
        if stytle == '外審版':
            self.find_Audit_page_and_merge()

    
    def find_Stamp_page(self):
        self.special_chapter_file_path = deepcopy(self.special_chapter_dic[1][0])
        self.special_chapter_dic.clear()
        for i in range(1, len(Stamp_ver_Chapter_1_2_data)):
            self.special_chapter_dic[i] = {}
            self.special_chapter_dic[i][0] = {'title' : Stamp_ver_Chapter_1_2_data[i]['title'], 'page' : None}
            
        title_1_2_list = list(deepcopy(Stamp_ver_Chapter_1_2_data[1]['inner_title']))
        title_1_2_list.extend(list(deepcopy(Stamp_ver_Chapter_1_2_data[2]['inner_title'])))

        PdfReader = PdfFileReader(self.special_chapter_file_path)
        total_page = PdfReader.getNumPages()
        self.special_chapter_dic['total_page'] =total_page
        
        for pages in range(total_page):
            Page_n = PdfReader.getPage(pages)
            txt = Page_n.extractText()
            while len(title_1_2_list) != 0:
                title = title_1_2_list[0]
                title_name = title.split('．')[1]
                pattern = re.compile(fr"(\d).(\d\d*)．({title_name})", re.I)
                find_pattern = pattern.findall(txt)
                if len(find_pattern) != 0:
                    chapter = int(find_pattern[0][0])
                    name = f"{find_pattern[0][0]}-{find_pattern[0][1]} {find_pattern[0][2]}"
                    self.special_chapter_dic[chapter][int(find_pattern[0][1])] = {'title': name, 'page': pages + 1}
                    index_title = title_1_2_list.index(title)
                    title_1_2_list.pop(index_title)
                else:
                    break

        if len(title_1_2_list) != 0:
            raise NotFoundErr(f'WORNING! {self.special_chapter_file_path}中，章節{title_1_2_list[0]}未被找到，請檢查檔案')


    def find_Audit_page_and_merge(self):
        special_chapter_file_list = deepcopy(self.special_chapter_dic[1])
        self.special_chapter_dic.clear()
        merger = PdfMerger()
        self.special_chapter_dic[1] = {}
        self.special_chapter_dic[1][0] = {'title' : Audit_ver_Chapter_1_inner_title[1]['title'], 'page' : None}
        origin_title = Audit_ver_Chapter_1_inner_title[1]['inner_title'].split('_')
        now_pages = 1
        for file_list_num in range(len(special_chapter_file_list)):
            PdfReader = PdfFileReader(special_chapter_file_list[file_list_num])
            merger.append(special_chapter_file_list[file_list_num])
            page = PdfReader.getNumPages()
            title = f'{origin_title}{Chapter_number[file_list_num + 1]}'
            special_chapter_file_list[1][file_list_num + 1] = {'title' : title, 'page' : now_pages}
            now_pages += page

        self.special_chapter_dic['total_page'] = now_pages - 1
        file_name = 'First_Chapter.pdf'
        self.special_chapter_file_path = os.path.join(self.output_path, file_name)  
        merger.write(self.special_chapter_file_path)
        merger.close()


    def add_same_and_special_chapter(self):
        now_pages = self.special_chapter_dic.pop('total_page')
        chapter_count = 1
        for i in range(1, len(self.special_chapter_dic)+1):
            self.all_chapter_dic[chapter_count] = self.special_chapter_dic.pop(i)
            chapter_count += 1

        self.same_chapter_flag = chapter_count
        now_pages += 1
        self.get_same_chapter_page_cover_page(chapter_count, now_pages)

        for chapter in list(self.same_chapter_dic.keys()):
            self.all_chapter_dic[chapter_count] = self.same_chapter_dic.pop(chapter)
            chapter_count += 1
            

    def get_same_chapter_page_cover_page(self, chapter_count, now_pages):
        for chapter, data in self.same_chapter_dic.items():
            for key, values in data.items():
                if key == 0:
                    cover_chapter = Chapter_number[chapter_count]
                    cover_name =  self.same_chapter_dic[chapter][0]['title']
                    pdf_output_path = self.generate_cover_pdf(cover_chapter, cover_name)
                    self.same_chapter_dic[chapter][0]['pdf_path'] = pdf_output_path

                PdfReader = PdfFileReader(values['pdf_path'])
                get_page = PdfReader.getNumPages()
                self.same_chapter_dic[chapter][key]['page'] = now_pages 
                now_pages += get_page

            chapter_count += 1


    def generate_cover_pdf(self, chapter, name):
        tmp_dic = {}
        tmp_dic['chapter'] = chapter
        tmp_dic['title'] = name
        doc_output_path = word_pdf.write_cover_word(self.output_path, f'cover_{chapter}', tmp_dic)
        pdf_output_path = word_pdf.turn_word_to_pdf(doc_output_path)

        self.delete_file_list.append(doc_output_path)
        self.delete_file_list.append(pdf_output_path)
        return pdf_output_path 


    def get_output_file_path(self):
        now_date = datetime.date.today()
        file_name = f'{now_date}_merge.pdf'
        self.output_merge_pdf_path = os.path.join(self.output_path, file_name)    

    def merge_all_pdf(self):
        merger = PdfMerger()
        merger.append(self.special_chapter_file_path)
        for chapter in range(self.same_chapter_flag, len(self.all_chapter_dic)+1):
            for key, value in self.all_chapter_dic[chapter].items():
                merger.append(value.pop('pdf_path'))
        
        self.get_output_file_path()
        merger.write(self.output_merge_pdf_path)
        merger.close()
        self.delete_file()

    
    def transfer_to_word_stytle(self):
        if stytle == '核章版':
            self.transfer_to_word_stytle_Stamp_chapter()
        if stytle == '外審版':
            pass   
        
        self.transfer_to_word_stytle_same_chapter()
        

    def transfer_to_word_stytle_Stamp_chapter(self):
        temp_list = []
        for chapter in range(1, self.same_chapter_flag):
            temp_dic = {}
            temp_inner_list = []
            temp_dic['big_title'] = f"{Chapter_number[chapter]}、{self.all_chapter_dic[chapter][0]['title']}"
            if chapter >= self.same_chapter_flag:
                temp_dic['page'] = self.all_chapter_dic[chapter][0]['page']
            for inner_chapter in range(1, len(self.all_chapter_dic[chapter])):
                if not self.all_chapter_dic[chapter][inner_chapter]['title']:
                    temp_inner_list = []
                else:
                    temp_inner_list.append(deepcopy(self.all_chapter_dic[chapter][inner_chapter]))
            
            temp_dic['inner_title'] = deepcopy(temp_inner_list)
            temp_list.append(deepcopy(temp_dic))
            self.to_word_outline['title_special'] = deepcopy(temp_list)

    
    def transfer_to_word_stytle_same_chapter(self):
        temp_list = []
        for chapter in range(self.same_chapter_flag, len(self.all_chapter_dic)+1):
            temp_dic = {}
            temp_inner_list = []
            temp_dic['big_title'] = f"{Chapter_number[chapter]}、{self.all_chapter_dic[chapter][0]['title']}"
            if chapter >= self.same_chapter_flag:
                temp_dic['page'] = self.all_chapter_dic[chapter][0]['page']
            for inner_chapter in range(1, len(self.all_chapter_dic[chapter])):
                if not self.all_chapter_dic[chapter][inner_chapter]['title']:
                    temp_inner_list = []
                else:
                    temp_inner_list.append(deepcopy(self.all_chapter_dic[chapter][inner_chapter]))
            
            temp_dic['inner_title'] = deepcopy(temp_inner_list)
            temp_list.append(deepcopy(temp_dic))

            if chapter == self.same_chapter_flag-1:
                self.to_word_outline['title_special'] = deepcopy(temp_list)
                del temp_list[:]
            if chapter == len(self.all_chapter_dic):
                self.to_word_outline['title_same'] = deepcopy(temp_list)
                del temp_list[:]
    
    def delete_file(self):
        for file in self.delete_file_list:
            os.remove(file)


def Merge_Final_PDF(Outline_pdf_path, Merged_pdf_path, number, final_file_name):
    tmp_final_pdf_path = Outline_pdf_path.split('\\')[:-1]
    final_pdf_path = '\\'.join(tmp_final_pdf_path)
    if final_file_name:
        final_pdf_name = f'{final_file_name}.pdf'
    else:
        final_pdf_name = f'{number}_結構計算書(全).pdf'
    final_path = os.path.join(final_pdf_path, final_pdf_name)
    merger = PdfMerger(strict = False)
    merger.append(Outline_pdf_path)
    merger.append(Merged_pdf_path)
    merger.write(final_path)
    merger.close()
    return final_path

          


if "__main__" == __name__:
    pdf = Merge_Pdf_and_GetOutline(r'E:\python\github\Tool\pdf_merge\整合PDF(all)\整合前', r'E:\python\github\Tool\pdf_merge\整合PDF(all)\整合前\merge_file')
    pdf.create_order_dic()
    pdf.find_special_chapter_file()
    pdf.find_same_chapter_file()
    pdf.order_same_chpater()
   
    pdf.find_special_chapter_page()
    pdf.add_same_and_special_chapter()
    print(pdf.same_chapter_dic)
    print(pdf.special_chapter_dic)
    #print(pdf.special_chapter_file_path)
    pdf.merge_all_pdf()
    #print(pdf.all_chapter_dic)
    pdf.transfer_to_word_stytle()
    print(pdf.to_word_outline)
    
    


