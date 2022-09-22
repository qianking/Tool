from xml.dom import NotFoundErr
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
#共通有的章節
All_Same_Chapter = {
        3: {'title': '結構設計檢核', 'inner_title_and_file_name':
                ['軟層檢核', 
                '剪力牆設計', 
                '一樓樓版剪力傳遞', 
                '梁上柱檢核', 
                '梁柱韌性與扭力檢核', 
                '極限層剪力檢核', 
                'SRC梁檢核', 
                'SRC柱檢核', 
                '上浮力檢核', 
                '地下室外牆設計', 
                '無梁版檢核', 
                '基礎設計',
                '逆打基樁檢核',
                '逆打鋼柱檢核']},
        4: {'title': '開挖設計', 'inner_title_and_file_name': None},
        5: {'title': '結構外審意見回覆', 'inner_title_and_file_name':
                ['第一次意見回覆',
                '第二次意見回覆',
                '第三次意見回覆',
                '會後意見回覆']},
        6: {'title': '設計分析報表', 'inner_title_and_file_name':
                ['大梁、柱、牆',
                '小梁、版']}  
    }


#核章版
''' Stamp_ver_Chapter_1_2_data = \
{0: {'file_name': '地震風力'},
1:{'title': '設計概要說明', 'inner_title' : ('1-1．建築概要','1-2．結構系統', '1-3．結構模型示意圖', '1-4．設計規範', '1-5．主要材料強度', '1-6．設計載重', '1-7．構材尺寸', '1-8．分析程式', '1-9．載重組合', '1-10．地震作用時層間變位檢討', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心')},
2: {'title': '地震力與風力計算', 'inner_title' :('2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算')}} '''

Stamp_ver_Chapter_1_2_data = {
    1:{'title': '設計概要說明', 'inner_title' : ('1-1．建築概要','1-2．結構系統', '1-3．結構模型示意圖', '1-4．設計規範', '1-5．主要材料強度', '1-6．設計載重', '1-7．構材尺寸', '1-8．分析程式', '1-9．載重組合', '1-10．地震作用時層間變位檢討', '1-11．建築物重量計算', '1-12．動力分析週期', '1-13．振態說明', '1-14．剛性隔板質心及剛心')},
    2: {'title': '地震力與風力計算', 'inner_title' :('2-1．建築物設計地震力計算', '2-2．垂直地震力計算', '2-3．建築物地震力之豎向分配', '2-4．動力反應譜分析調整放大係數', '2.5．動力分析樓層剪力', '2.6．動力分析質心位移', '2.7．動力分析層間變位角', '2.8．意外扭矩放大係數計算', '2-9．碰撞間隔及層間變位角計算', '2-10．風力計算')}
}

#外審版
Audit_ver_Chapter_1_inner_title = \
{1:{'title': '外審意見回覆', 'inner_title' :'附件'}}


Chapter_number = \
{1: '一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六'}

#stytle = '外審版'

#stytle =['核章版': Stamp_single、Stamp_multi, '外審版': Audit]


class Merge_Pdf_and_GetOutline():
    def __init__(self, pdf_data):
        self.pdf_data = pdf_data
        self.file_list = glob(f"{self.pdf_data['input_folder_path']}\*.pdf")
        self.debug_file = deepcopy(self.file_list)
        self.special_chapter_file_path = ''
        self.same_chapter_flag = None
        self.delete_file_list = []
        self.all_chapter_dic = {}
        self.to_word_outline = {}
        

    def create_order_dic(self):
        self.same_chapter_dic = {}
        len_order = len(Chapter_number)
        for chapter in range(1, len_order+1):
            self.same_chapter_dic[chapter] = {}

        self.special_chapter_dic = {1:[]}


    def find_same_chapter_file(self):
        for pdf in self.file_list:
            pdf_file = self.find_the_same_chapter(pdf)
            if pdf_file:
                index = self.debug_file.index(pdf)
                self.debug_file.pop(index)
        
        if len(self.debug_file)!= 0:
            bug_file = '、'.join(self.debug_file)
            raise FileNotFoundError(f'WORNING! 有檔案未被合併 : {bug_file}，請檢查檔案並重新選擇資料夾!')


    def find_the_same_chapter(self, pdf):
        pdf_name = pdf.split('\\')[-1]   #得到pdf名子
        for chapter, chapter_data in All_Same_Chapter.items():
                file_NO_pattern = re.compile(fr"^\d[{chapter}]_(\d\d)", re.I)
                find = file_NO_pattern.findall(pdf_name)
                if len(find):
                    index_inner = int(find[0])
                    if chapter_data['inner_title_and_file_name']:
                        self.same_chapter_dic[chapter][index_inner] = {'title': chapter_data['inner_title_and_file_name'][index_inner-1], 'pdf_path': pdf}
                    else:
                        self.same_chapter_dic[chapter][index_inner] = {'title': None, 'pdf_path': pdf}

                    self.same_chapter_dic[chapter][0] = {'title': chapter_data['title']}
                    return pdf    
            

    ''' def find_the_same_chapter(self, pdf):
        pdf_name = pdf.split('\\')[-1]   #得到pdf名子
        for chapter, file_name_list in All_same_chapter.items():
            if file_name_list['inner_title_and_file_name']:     #如果該章節檔案名稱不是使用該章節的title名稱命名
                for i, file_data in enumerate(file_name_list['inner_title_and_file_name']):
                    for name in file_data['file_name']:
                        if name in pdf_name:
                            pdf_path = os.path.join(self.pdf_data['input_folder_path'], pdf_name)
                            self.same_chapter_dic[chapter][i+1] = {'title': file_data['title'], 'pdf_path': pdf_path}
                            self.same_chapter_dic[chapter][0] = {'title': file_name_list['title']}
                            return pdf
            else:                                                   #如果該章節檔案名稱是使用該章節的title名稱命名
                file_name = file_name_list['file_name']  
                if file_name in pdf_name:
                    pdf_path = os.path.join(self.pdf_data['input_folder_path'], pdf_name)
                    self.same_chapter_dic[chapter][1] = {'title': None, 'pdf_path': pdf_path}
                    self.same_chapter_dic[chapter][0] = {'title': file_name_list['title']}
                    return pdf '''

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
        find_file_flag = False
        file_NO_special_pattern = re.compile(r"^\d[1,2]_\d\d", re.I)
        for pdf_path in self.file_list:
            pdf_name = pdf_path.split('\\')[-1]
            find_pattern = file_NO_special_pattern.findall(pdf_name)
            if len(find_pattern):
                self.special_chapter_dic[1].append(pdf_path)
                index = self.debug_file.index(pdf_path)
                self.debug_file.pop(index)
                find_file_flag = True

        if not find_file_flag:
            raise FileNotFoundError(f"WORNING! 找不到{self.pdf_data['select_stytle']}第一章檔案! 請檢查檔案和選擇合併版本並重新選擇資料夾")
        
        if self.pdf_data['select_stytle'] == 'Stamp_multi':
            if len(self.pdf_data['build_no']) > len(self.special_chapter_dic[1]):
                raise FileNotFoundError(f"WORNING! 核章版多棟版本第一章有檔案缺少或是建築編號多填，請檢查輸入參數或檔案")
            elif len(self.pdf_data['build_no']) < len(self.special_chapter_dic[1]):
                raise FileNotFoundError(f"WORNING! 核章版多棟版本第一章有建築編號少填，請檢查輸入參數或檔案")
            else:
                Stamp_multi_chapter_file_list = []
                debug_special_chapter_file = deepcopy(self.special_chapter_dic[1])      #將核章版多棟第一章檔案名稱跟使用者填寫的建築編號做一個確認並且排序整齊
                for no in range(1, (len(self.pdf_data['build_no']))+1):
                    if no < 10:
                        no = str(f'0{no}')
                    else:
                        no = str(no)
                    file_name_pattern = re.compile(fr"^\d[2]_{no}", re.I)
                    for pdf_path in self.special_chapter_dic[1]:
                        find_pattern = file_name_pattern.findall(pdf_path.split('\\')[-1])
                        if len(find_pattern):
                            index = debug_special_chapter_file.index(pdf_name)
                            p = debug_special_chapter_file.pop(index)
                            Stamp_multi_chapter_file_list.append(p)
                            break

                if len(debug_special_chapter_file) != 0:
                    raise FileNotFoundError(f"WORNING! 核章版多棟版本第一章有檔案命名有誤或是建築編號填寫錯誤，請檢查輸入參數或檔案") 
                else:
                    self.special_chapter_dic[1] = deepcopy(Stamp_multi_chapter_file_list)  
               
       
    def find_special_chapter_page(self):
        if self.pdf_data['select_stytle'] == 'Stamp_single':
            self.find_Stamp_single_page()
        if self.pdf_data['select_stytle'] == 'Stamp_multi':
            self.find_Stamp_multi_page()
            self.merge_Stamp_multi_file()
        if self.pdf_data['select_stytle'] == 'Audit':
            self.find_Audit_page_and_merge()

        self.delete_file_list.append(self.special_chapter_file_path)

    
    def find_Stamp_single_page(self):
        self.special_chapter_file_path = deepcopy(self.special_chapter_dic[1][0])
        self.special_chapter_dic.clear()
        for i in range(1, len(Stamp_ver_Chapter_1_2_data)+1):
            self.special_chapter_dic[i] = {}
            self.special_chapter_dic[i][0] = {'title' : Stamp_ver_Chapter_1_2_data[i]['title'], 'page' : None}
            
        title_1_2_list = list(deepcopy(Stamp_ver_Chapter_1_2_data[1]['inner_title']))
        title_1_2_list.extend(list(Stamp_ver_Chapter_1_2_data[2]['inner_title']))
        debug_title_list = deepcopy(title_1_2_list)
        PdfReader = PdfFileReader(self.special_chapter_file_path)
        total_page = PdfReader.getNumPages()
        self.special_chapter_dic['total_page'] =total_page
        
        for pages in range(total_page):
            Page_n = PdfReader.getPage(pages)
            txt = Page_n.extractText()
            if len(title_1_2_list) != 0:
                for title in title_1_2_list:
                    title_name = title.split('．')[1]
                    pattern = re.compile(fr"(\d).(\d\d*)．({title_name})", re.I)
                    find_pattern = pattern.findall(txt)
                    if len(find_pattern) != 0:
                        chapter = int(find_pattern[0][0])
                        name = f"{find_pattern[0][0]}-{find_pattern[0][1]} {find_pattern[0][2]}"
                        self.special_chapter_dic[chapter][int(find_pattern[0][1])] = {'title': name, 'page': pages + 1}
                        index_title = debug_title_list.index(title)
                        debug_title_list.pop(index_title)
                        continue
                    if title == title_1_2_list[-1]:
                        break
     
        if len(debug_title_list) != 0:
            fail_title = '、'.join(debug_title_list)
            raise NotFoundErr(f'WORNING! {self.special_chapter_file_path}中，章節{fail_title}未被找到，請檢查檔案中標題名稱!')


    def find_Stamp_multi_page(self):
        special_chapter_file_list = deepcopy(self.special_chapter_dic[1])
        self.special_chapter_dic.clear()
        build_NO = self.pdf_data['build_no']
        
        title_1_2_list = list(deepcopy(Stamp_ver_Chapter_1_2_data[1]['inner_title']))
        title_1_2_list.extend(list(deepcopy(Stamp_ver_Chapter_1_2_data[2]['inner_title'])))

        same_title_1_2 = set(title_1_2_list[:10])      #1-1 ~ 1-10為所有檔案都有的，拿來做為查看是否有漏掉title用
        self.special_chapter_dic = {}
        debug_title_dic = {}
        
        for i, pdf in enumerate(special_chapter_file_list):
            debug_title_list = deepcopy(title_1_2_list)

            PdfReader = PdfFileReader(pdf)
            total_page = PdfReader.getNumPages()
            self.special_chapter_dic[build_NO[i]] = {"pdf" : pdf, "total_page" : total_page, 1 : {0:{'title' : Stamp_ver_Chapter_1_2_data[1]['title'], 'page' : None}}, 2 : {0:{'title' : Stamp_ver_Chapter_1_2_data[2]['title'], 'page' : None}}}
            
            for pages in range(total_page):
                Page_n = PdfReader.getPage(pages)
                txt = Page_n.extractText()

                if len(title_1_2_list) != 0:
                    for title in title_1_2_list:
                        title_name = title.split('．')[1]
                        pattern = re.compile(fr"(\d).(\d\d*)．({title_name})", re.I)
                        find_pattern = pattern.findall(txt)
                        if len(find_pattern) != 0:
                            chapter = int(find_pattern[0][0])
                            name = f"{find_pattern[0][0]}-{find_pattern[0][1]} {find_pattern[0][2]}"
                            self.special_chapter_dic[build_NO[i]][chapter][int(find_pattern[0][1])] = {'title': name, 'page': pages + 1}
                            index_title = debug_title_list.index(title)
                            debug_title_list.pop(index_title)
                            continue
                        if title == title_1_2_list[-1]:
                            break
            
            if set(debug_title_list) & same_title_1_2 == same_title_1_2: 
                debug_title_list = list(set(debug_title_list) - same_title_1_2)
            if len(debug_title_list):
                debug_title_dic[i] = {'pdf' : pdf, 'fail_title_list' : deepcopy(debug_title_list)}
        
        if len(debug_title_dic):
            txt  = ''
            for i, data in debug_title_dic.items():
                title_txt = '、'.join(data['fail_title_list'])
                txt += f"{data['pdf']}中，章節{title_txt}未被找到，\n"
            raise NotFoundErr(f'WORNING! {txt}，請檢查檔案中標題名稱!')
    
    def merge_Stamp_multi_file(self):
        #print('\nspecial_chapter_dic', self.special_chapter_dic)
        special_chapter_data = {}
        have_1_10_file = {}
        for no, data in self.special_chapter_dic.items():                 #先找到有第1-1~1-10章節的檔案
            if 1 in data[1]:
                have_1_10_file[no] = {'pdf' : data['pdf'], 1:{}}        #把有1-1~1-10章節的檔案存起來
                for i in range(11):
                    have_1_10_file[no][1][i] = data[1].pop(i)
                total_page_1_10 = data[1][11]['page']-1
                have_1_10_file[no]['total_page'] = total_page_1_10
        if not len(have_1_10_file):
            raise NotFoundErr(f'WORNING! 並未找到1-1 ~ 1-10章節')
        if len(have_1_10_file) > 1:
            debug_list = []
            for no, data in have_1_10_file.items():
                debug_list.append(data[1][10]['page'])
                if len(set(debug_list)) > 1:
                    raise NotFoundErr(f'WORNING! 有檔案第1-10章節頁數不同')

        #print('\nhave_1_10_file', have_1_10_file)
        frist = list(have_1_10_file.keys())[0]
        frist_file = have_1_10_file[frist]['pdf']
        PdfReader = PdfFileReader(frist_file)
        first_chapter_file = PdfFileWriter()
        for pages in range(total_page_1_10):        #先將1-1~1-10提取出來寫入檔案
            page = PdfReader.getPage(pages)
            first_chapter_file.addPage(page)
        special_chapter_data[1] = have_1_10_file[frist][1]
        special_chapter_data[2] = {}
        now_page = total_page_1_10

        for no, data in self.special_chapter_dic.items():
            PdfReader = PdfFileReader(data['pdf'])
            special_chapter_data[2][no] = {}
            if 0 in data[1]:
                del data[1][0]
            chapter_list = list(data[1]) 
            frist_page_chapter = chapter_list[0]
            pdf_fisrt_page = data[1][frist_page_chapter]['page']
            for i in range(pdf_fisrt_page-1, data['total_page']): #將1-10之後的章節全合併起來
                page = PdfReader.getPage(i)
                first_chapter_file.addPage(page)
                

            for chapter in range(1, 3):
                special_chapter_data[2][no][chapter] = {}
                chapter_list = list(data[chapter])
                for chap in chapter_list:
                    tmp_dic = deepcopy(data[chapter][chap])
                    
                    if tmp_dic['page']:                           #如果為封面頁，代表那頁沒頁碼，如果不是封面，那代表有頁碼
                        if pdf_fisrt_page != 1:
                            if tmp_dic['page']:
                                tmp_dic['page'] = tmp_dic['page'] - total_page_1_10 + now_page
                        elif pdf_fisrt_page == 1:
                            tmp_dic['page'] += now_page

                    special_chapter_data[2][no][chapter][chap] = deepcopy(tmp_dic)

            if data[1][11]['page'] != 1:
                now_page = data['total_page'] - total_page_1_10 + now_page
            else:
                now_page += data['total_page']
        

        self.special_chapter_dic = special_chapter_data
        self.special_chapter_dic['total_page'] = now_page 
        self.special_chapter_file_path = os.path.join(self.pdf_data['tmp_file_folder_path'], 'first_chapter_pdf.pdf') 

        with open(self.special_chapter_file_path, 'wb') as f:
            first_chapter_file.write(f)


    def find_Audit_page_and_merge(self):
        special_chapter_file_list = deepcopy(self.special_chapter_dic[1])
        self.special_chapter_dic.clear()
        merger = PdfMerger()
        self.special_chapter_dic[1] = {}
        self.special_chapter_dic[1][0] = {'title' : Audit_ver_Chapter_1_inner_title[1]['title'], 'page' : None}
        origin_title = Audit_ver_Chapter_1_inner_title[1]['inner_title']
        now_pages = 1
        for file_list_num, file_path in enumerate(special_chapter_file_list):
            PdfReader = PdfFileReader(file_path)
            merger.append(file_path)
            page = PdfReader.getNumPages()
            title = f'{str(file_list_num + 1)}.  {origin_title}{Chapter_number[file_list_num + 1]}'
            self.special_chapter_dic[1][file_list_num + 1] = {'title' : title, 'page' : now_pages}
            now_pages += page

        self.special_chapter_dic['total_page'] = now_pages - 1
        file_name = 'First_Chapter.pdf'
        self.special_chapter_file_path = os.path.join(self.pdf_data['tmp_file_folder_path'], file_name)  
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
            self.all_chapter_dic[chapter_count] = deepcopy(self.same_chapter_dic[chapter])
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
        doc_output_path = word_pdf.write_cover_word(self.pdf_data['tmp_file_folder_path'], tmp_dic, f'cover_{chapter}')
        pdf_output_path = word_pdf.turn_word_to_pdf(doc_output_path)

        self.delete_file_list.append(doc_output_path)
        self.delete_file_list.append(pdf_output_path)
        return pdf_output_path 


    def get_output_file_path(self):
        now_date = datetime.date.today()
        file_name = f'{now_date}_merge.pdf'
        self.output_merge_pdf_path = os.path.join(self.pdf_data['tmp_file_folder_path'], file_name)    

    def merge_all_pdf(self):
        merger = PdfMerger()
        merger.append(self.special_chapter_file_path)
        for chapter in range(self.same_chapter_flag, len(self.all_chapter_dic)+1):
            for key, value in self.all_chapter_dic[chapter].items():
                merger.append(value.pop('pdf_path'))
        
        self.get_output_file_path()
        merger.write(self.output_merge_pdf_path)
        merger.close()
        self.delete_file_list.append(self.output_merge_pdf_path)
    
    def transfer_to_word_stytle(self):
        if self.pdf_data['select_stytle'] == 'Stamp_single' or self.pdf_data['select_stytle'] == 'Audit':
            self.transfer_to_word_stytle_Stamp_single_chapter()

        if self.pdf_data['select_stytle'] == 'Stamp_multi':  
            self.transfer_to_word_stytle_Stamp_multi_chapter()

        self.transfer_to_word_stytle_same_chapter()
        

    def transfer_to_word_stytle_Stamp_single_chapter(self):
        temp_list = []
        for chapter in range(1, self.same_chapter_flag):
            temp_dic = {}
            temp_inner_list = []
            temp_dic['big_title'] = f"{Chapter_number[chapter]}、{self.all_chapter_dic[chapter][0]['title']}"

            if self.all_chapter_dic[chapter][0]['page']:
                temp_dic['page'] = self.all_chapter_dic[chapter][0]['page']

            for inner_chapter in range(1, len(self.all_chapter_dic[chapter])):
                if not self.all_chapter_dic[chapter][inner_chapter]['title']:
                    temp_inner_list = []
                else:
                    temp_inner_list.append(deepcopy(self.all_chapter_dic[chapter][inner_chapter]))
            
            temp_dic['inner_title'] = deepcopy(temp_inner_list)
            temp_list.append(deepcopy(temp_dic))
            self.to_word_outline['title_special'] = deepcopy(temp_list)
        del temp_list[:]

    
    def transfer_to_word_stytle_Stamp_multi_chapter(self):
        temp_list = []
        temp_dic = {}
        temp_inner_list = []
        temp_dic['big_title'] = f"{Chapter_number[1]}、{self.all_chapter_dic[1][0]['title']}"
        for inner_chapter in range(1, len(self.all_chapter_dic[1])):   
            temp_inner_list.append(deepcopy(self.all_chapter_dic[1][inner_chapter]))
        temp_dic['inner_title'] = deepcopy(temp_inner_list)
        temp_list.append(deepcopy(temp_dic))
        self.to_word_outline['title_special_1'] = deepcopy(temp_list)

        del temp_list[:]
        del temp_inner_list[:]
        temp_dic.clear()

        chapter_2 = self.all_chapter_dic[2]
        for no, data in chapter_2.items():
            temp_dic['build_titie'] = f"{no}棟"
            for inner_chapter, inner_data in data[1].items():
                temp_inner_list.append(deepcopy(inner_data))
            temp_dic['inner_1_title'] = deepcopy(temp_inner_list)
            del temp_inner_list[:]
            for inner_chapter, inner_data in data[2].items():
                if inner_chapter == 0:
                    temp_dic['big_title'] = f"{Chapter_number[2]}、{inner_data['title']}"
                else:
                    temp_inner_list.append(deepcopy(inner_data))
            temp_dic['inner_2_title'] = deepcopy(temp_inner_list)
            temp_list.append(deepcopy(temp_dic))
            del temp_inner_list[:]
        self.to_word_outline['title_special_2'] = deepcopy(temp_list)
     
    
    def transfer_to_word_stytle_same_chapter(self):
        temp_list = []
        for chapter in range(self.same_chapter_flag, len(self.all_chapter_dic)+1):
            temp_dic = {}
            temp_inner_list = []
            temp_dic['big_title'] = f"{Chapter_number[chapter]}、{self.all_chapter_dic[chapter][0]['title']}"
    
            if self.all_chapter_dic[chapter][0]['page']:
                temp_dic['page'] = self.all_chapter_dic[chapter][0]['page']

            for inner_chapter in range(1, len(self.all_chapter_dic[chapter])):
                if not self.all_chapter_dic[chapter][inner_chapter]['title']:
                    temp_inner_list = []
                else:
                    temp_inner_list.append(deepcopy(self.all_chapter_dic[chapter][inner_chapter]))
            
            temp_dic['inner_title'] = deepcopy(temp_inner_list)
            temp_list.append(deepcopy(temp_dic))
            self.to_word_outline['title_same'] = deepcopy(temp_list)
        del temp_list[:]


def Merge_Final_PDF(Outline_pdf_path, Merged_pdf_path, number, final_file_name):
    tmp_final_pdf_path = Outline_pdf_path.split('\\')[:-1]
    final_pdf_path = '\\'.join(tmp_final_pdf_path)
    if final_file_name:
        final_pdf_name = f'{final_file_name}.pdf'
    else:
        final_pdf_name = f'{number}_結構計算書.pdf'
    final_path = os.path.join(final_pdf_path, final_pdf_name)
    merger = PdfMerger(strict = False)
    merger.append(Outline_pdf_path)
    merger.append(Merged_pdf_path)
    merger.write(final_path)
    merger.close()
    return final_path

          


if "__main__" == __name__:
    pdf = Merge_Pdf_and_GetOutline('外審版', r'C:\Users\andy_chien\Downloads\整合PDF(all)0802\整合前\外審版', r'C:\Users\andy_chien\Downloads\整合PDF(all)0802\整合前\外審版\2022-08-03_merger')
    pdf.create_order_dic()
    pdf.find_special_chapter_file()
    pdf.find_same_chapter_file()
    pdf.order_same_chpater()
   
    pdf.find_special_chapter_page()
    pdf.add_same_and_special_chapter()
    print('same_chapter_dic:', pdf.same_chapter_dic)
    print('special_chapter_dic:',pdf.special_chapter_dic)
    print('special_chapter_file_path:',pdf.special_chapter_file_path)
    pdf.merge_all_pdf()
    print('all_chapter_dic:',pdf.all_chapter_dic)
    pdf.transfer_to_word_stytle()
    print('to_word_outline:', pdf.to_word_outline)
    
    


