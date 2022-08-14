import os
import pdf_merger_2 as merger
import write_word_pdf as word_pdf
from glob import glob
import datetime
import comtypes.client
import time

outline_information = {}
pdf_information = {}

self = None
status = None

def send_msg_to_UI(msg):
    if self:
        self.status.emit(msg)

def get_variable_form_UI(outline_infor, pdf_infor):
    global self
    global status
    global pdf_information
    global outline_information
    outline_information = outline_infor
    outline_information['number'] = f"V{str(outline_infor['number'])}"

    pdf_information = pdf_infor
    self = pdf_infor.get('self')
    status = pdf_infor.get('status')


def create_merger_folder():
    now_date = datetime.date.today()
    tmp_file_folder_path = os.path.join(pdf_information['input_folder_path'], f'{now_date}_merger')
    if not os.path.isdir(tmp_file_folder_path):
        os.makedirs(tmp_file_folder_path)
    pdf_information['tmp_file_folder_path'] = tmp_file_folder_path


def merge_pdf():
    create_merger_folder()
    pdf = merger.Merge_Pdf_and_GetOutline(pdf_information)
    pdf.create_order_dic()
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
    return merge_pdf_path, outline_data

def get_outline_pdf(outline_data):
    outline_data['number'] = outline_information['number']
    outline_data['address'] = outline_information['address']
    outline_data['name'] = outline_information['name']
    if pdf_information['select_stytle'] == 'Audit':
        outline_data['outline_title'] = pdf_information['Audit_selection']
    outline_doc_path = word_pdf.write_outline_word(pdf_information['select_stytle'], pdf_information['tmp_file_folder_path'], outline_data)
    outline_pdf_path = word_pdf.turn_word_to_pdf(outline_doc_path)

    return outline_pdf_path


def main(basic_data, special_data):
    try:
        start_time = time.time()
        get_variable_form_UI(basic_data, special_data)
        
        send_msg_to_UI('合併開始...')
        create_merger_folder()

        send_msg_to_UI('生成合併pdf檔...')
        merge_pdf_path, outline_data = merge_pdf()
        time.sleep(0.5)

        send_msg_to_UI('生成封面pdf檔...')
        outline_pdf_path = get_outline_pdf(outline_data)
        time.sleep(0.5)
        
        send_msg_to_UI('生成最終檔案...')
        final_path = merger.Merge_Final_PDF(outline_pdf_path, merge_pdf_path, outline_information['number'], outline_information['file_name'])
         
    except Exception as ex:
        print(ex)
        msg = str(ex)
        if 'WORNING' not in msg:
            msg = f'ERROR! 錯誤 : {msg}'
        send_msg_to_UI(msg)
        return 0

    else:
        end_time = time.time()
        cost_time = str(end_time- start_time)
        cost_time = cost_time.split('.')[0]
        msg = f'合併完成!\n生成路徑 : {final_path}\nCost : {cost_time} s'
        send_msg_to_UI(msg)


if "__main__" == __name__:
    pdf_information = {'select_stytle': 'Stamp_multi', 'build_num': 4, 'build_no': ['1', '2', '3', '4'], 'input_folder_path': 'E:\\python\\github\\Tool\\pdf_merge\\整合PDF(all)\\整合前\\核章版 多', 'self': '<__main__.Merge_PDF_Thread(0x2784804e4c0) at 0x000002783D58B100>', 'status': '<PySide6.QtCore.SignalInstance status(QString) at 0x000002783D581AB0>', 'tmp_file_folder_path': 'E:\\python\\github\\Tool\\pdf_merge\\整合PDF(all)\\整合前\\核章版 多\\2022-08-14_merger'}
    merge_pdf()