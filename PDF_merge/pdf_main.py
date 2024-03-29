import os
import sys
import pdf_merger as merger
import write_word_pdf as word_pdf
from PyPDF2 import PdfFileReader, PdfFileWriter
import datetime
import time
import traceback
import config_load
import addpagenumber

"""
檢查檔案存在(Template)

"""

outline_information = {}
pdf_information = {}

self = None
status = None

config_path = r".\config.ini"

def send_msg_to_UI(msg):
    if self:
        self.status.emit(msg)

def get_variable_form_UI(outline_infor, pdf_infor, config):
    global self
    global status
    global pdf_information
    global outline_information
    global config_path

    outline_information = outline_infor
    
    pdf_information = pdf_infor
    self = pdf_infor.get('self')
    status = pdf_infor.get('status')

    config_path = config

def get_merger_folder():
    #now_date = datetime.date.today()
    tmp_file_folder_path = '\\'.join(pdf_information['input_folder_path'].split('\\')[:-1])
    pdf_information['tmp_file_folder_path'] = tmp_file_folder_path

def merge_pdf():
    get_merger_folder()
    pdf = merger.Merge_Pdf_and_GetOutline(pdf_information)
    pdf.create_order_dic()  #創建字典
    pdf.find_special_chapter_file()     #需先找特殊檔案，因為找到特殊檔案後會先pop出來
    pdf.find_same_chapter_file()        #在找共通檔案
    pdf.order_same_chpater()
    pdf.find_special_chapter_page()
    print('special_chapter_dic:', pdf.special_chapter_dic)
    pdf.add_same_and_special_chapter()
    time.sleep(1)
    pdf.merge_all_pdf()
    print('\nall_chapter_dic:', pdf.all_chapter_dic)
    pdf.transfer_to_word_stytle() 
    print('\nto_word_outline:', pdf.to_word_outline)
    merge_pdf_path = pdf.output_merge_pdf_path
    outline_data = pdf.to_word_outline 
    delete_file_list = pdf.delete_file_list
    return merge_pdf_path, outline_data, delete_file_list

def get_outline_pdf(outline_data):
    outline_data['number'] = outline_information['number']
    outline_data['address'] = outline_information['address']
    outline_data['name'] = outline_information['name']
    if pdf_information['select_stytle'] == 'Audit':
        outline_data['outline_title'] = pdf_information['Audit_selection']
    outline_doc_path = word_pdf.write_outline_word(pdf_information['select_stytle'], pdf_information['tmp_file_folder_path'], outline_data)
    outline_pdf_path = word_pdf.turn_word_to_pdf(outline_doc_path)
    delete_blank_page(outline_pdf_path)
    return outline_pdf_path

def delete_blank_page(path):
    PdfReader = PdfFileReader(path)
    total_page = PdfReader.getNumPages()
    first_chapter_file = PdfFileWriter()
    for i in range(total_page):
        Page_n = PdfReader.getPage(i)
        txt = Page_n.extractText()
        txt = txt.strip()
        if txt != '':  
            first_chapter_file.addPage(Page_n)
    with open(path, 'wb') as f:
        first_chapter_file.write(f)
        
def delete_file(delete_list):
    for file in delete_list:
         os.remove(file)

def main(basic_data, special_data, config):
    #print('basic_data',basic_data)
    #print('special_data',special_data)
    #print('config',config)
    try:
        start_time = time.time()
        
        #獲取從UI傳入的參數和信號
        get_variable_form_UI(basic_data, special_data, config) 

        #讀取config中的資料
        All_Same_Chapter, Stamp_ver_Chapter_1_2_data, Audit_ver_Chapter_1_inner_title = config_load.load_ini(config_path)
        # print('All_Same_Chapter',All_Same_Chapter)
        # print('Stamp_ver_Chapter_1_2_data',Stamp_ver_Chapter_1_2_data)
        # print('Audit_ver_Chapter_1_inner_title',Audit_ver_Chapter_1_inner_title)

        #將config中，title名子合併到Stamp_ver_Chapter_1_2_data和Audit_ver_Chapter_1_inner_title全域變數中
        merger.get_title_data(All_Same_Chapter, Stamp_ver_Chapter_1_2_data, Audit_ver_Chapter_1_inner_title)
        
        send_msg_to_UI('合併開始...')

        send_msg_to_UI('生成合併pdf檔...')
        merge_pdf_path, outline_data, delete_file_list = merge_pdf()
        time.sleep(0.5)

        if pdf_information['page_num']:
            send_msg_to_UI('生成頁碼...')
            try:
                no_page_num_file, add_page_num_file = addpagenumber.add_page_number(merge_pdf_path)
                delete_file_list.append(no_page_num_file)
                delete_file_list.append(add_page_num_file)
                except_outline_file = add_page_num_file
            except Exception as ex:
                send_msg_to_UI(f'頁碼生成異常，改生成沒頁碼版本，請回饋給開發者\n EXCEPTION: {str(ex)}...')
                except_outline_file = merge_pdf_path
        else:
            except_outline_file = merge_pdf_path


        send_msg_to_UI('生成封面pdf檔...')
        outline_pdf_path = get_outline_pdf(outline_data)
        delete_file_list.append(outline_pdf_path)
        time.sleep(0.5)
        
        send_msg_to_UI('生成最終檔案...')
        final_path = merger.Merge_Final_PDF(outline_pdf_path, except_outline_file, outline_information['number'], outline_information['file_name'])

        delete_file(delete_file_list)
         
    except FileNotFoundError as ex:
        print(ex)
        msg = str(ex)
        if 'WORNING' not in msg:
            msg = f'ERROR! 錯誤 : {msg}'
        send_msg_to_UI(msg)
        return 0

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
        send_msg_to_UI(errMsg)
        return 0

    else:
        end_time = time.time()
        cost_time = str(end_time- start_time)
        cost_time = cost_time.split('.')[0]
        msg = f'合併完成!\n生成路徑 : {final_path}\nCost : {cost_time} s'
        send_msg_to_UI(msg)


if "__main__" == __name__:
    basic_data = {'number': 'V440', 'address': '555', 'name': '555', 'file_name': '555'}
    special_data = {'select_stytle': 'Stamp_multi', 'build_num': 2, 'build_no': ['A', 'B'], 'input_folder_path': 'C:\\Users\\Qian\\Downloads\\V440_計算書整合', 'page_num': False, 'self': None, 'status': None}
    #pdf_information = {'select_stytle': 'Stamp_multi', 'build_num': 4, 'build_no': ['1', '2', '3', '4'], 'input_folder_path': 'E:\\python\\github\\Tool\\pdf_merge\\整合PDF(all)\\整合前\\核章版 多', 'self': '<__main__.Merge_PDF_Thread(0x2784804e4c0) at 0x000002783D58B100>', 'status': '<PySide6.QtCore.SignalInstance status(QString) at 0x000002783D581AB0>', 'tmp_file_folder_path': 'E:\\python\\github\\Tool\\pdf_merge\\整合PDF(all)\\整合前\\核章版 多\\2022-08-14_merger'}
    main(basic_data, special_data, ".\config.ini")