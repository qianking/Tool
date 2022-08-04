import os
import pdf_merger_2 as merger
import write_word_pdf as word_pdf
from glob import glob
import datetime
import comtypes.client
import time

pdf_data = {}
special_pdf_data = {}

self = ''
status = ''

def send_msg_to_UI(msg):
    if self != '':
        self.status.emit(msg)

def get_variable_form_UI(basic_data, special_data):
    global self
    global status
    global special_pdf_data
    pdf_data['select_stytle'] = basic_data[0]
    pdf_data['number'] = f'V{str(basic_data[1])}'
    pdf_data['address'] = basic_data[2]
    pdf_data['name'] = basic_data[3]
    pdf_data['input_folder_path'] = basic_data[4]
    pdf_data['file_name'] = basic_data[5]
    special_pdf_data = special_data
    if 'self' in special_data:
        self = special_data['self']
        status = special_data['status']


def create_merger_folder():
    now_date = datetime.date.today()
    tmp_file_folder_path = os.path.join(pdf_data['input_folder_path'], f'{now_date}_merger')
    if not os.path.isdir(tmp_file_folder_path):
        os.makedirs(tmp_file_folder_path)
    pdf_data['tmp_file_folder_path'] = tmp_file_folder_path


def merge_pdf():
    pdf = merger.Merge_Pdf_and_GetOutline(pdf_data['select_stytle'], pdf_data['input_folder_path'], pdf_data['tmp_file_folder_path'])
    pdf.create_order_dic()
    pdf.find_special_chapter_file()     #需先找特殊檔案，因為找到特殊檔案後會先pop出來
    pdf.find_same_chapter_file()        #在找共通檔案
    pdf.order_same_chpater()
    pdf.find_special_chapter_page()
    pdf.add_same_and_special_chapter()
    time.sleep(1)
    pdf.merge_all_pdf()
    print('all_chapter_dic:', pdf.all_chapter_dic)
    pdf.transfer_to_word_stytle() 
    print('same_chapter_dic:', pdf.same_chapter_dic)
    print('special_chapter_file_path:', pdf.special_chapter_file_path)
    print('to_word_outline:', pdf.to_word_outline)
    merge_pdf_path = pdf.output_merge_pdf_path
    outline_data = pdf.to_word_outline
    return merge_pdf_path, outline_data

def get_outline_pdf(outline_data):
    outline_data['number'] = pdf_data['number']
    outline_data['address'] = pdf_data['address']
    outline_data['name'] = pdf_data['name']
    if pdf_data['select_stytle'] == '外審版':
        outline_data['outline_title'] = special_pdf_data['Audit_selection']
    outline_doc_path = word_pdf.write_outline_word(pdf_data['select_stytle'], pdf_data['tmp_file_folder_path'], 'Outline', outline_data)
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
        time.sleep(1)

        send_msg_to_UI('生成封面pdf檔...')
        outline_pdf_path = get_outline_pdf(outline_data)
        time.sleep(1)
        
        send_msg_to_UI('生成最終檔案...')
        final_path = merger.Merge_Final_PDF(outline_pdf_path, merge_pdf_path, pdf_data['number'], pdf_data['file_name'])
        
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
    main(('外審版', 554, '台中市西屯區福德段273、274地號集合住宅新建工程', '李明哲建築師事務所', r'C:\Users\andy_chien\Downloads\整合PDF(all)0802\整合前\外審版', 'test'), {'Audit_selection':'第二次外審結構計算書'})