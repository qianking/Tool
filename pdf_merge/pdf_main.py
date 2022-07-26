import write_word
import os
import pdf_merger
from glob import glob
import re
import datetime

self = ''
status = ''


def send_msg_to_UI(msg):
    if self != '':
        self.status.emit(msg)


def get_variable_form_UI(**args):
    global self
    global status
    if 'self' in args:
        self = args['self']
        status = args['status']
        return args['number'], args['address'], args['name'], args['folder']


def get_first_page_and_merge_pdf(number, address, name, folder_path):
    try:
        pdf = pdf_merger.Merge_Pdf_and_GetOutline(folder_path)
        pdf.order_file()
        if len(pdf.debug_file_list) != 0:
            print('debug_file_list:', pdf.debug_file_list)
            msg = f'WORNIG! 有檔案未被合併，檔案名 {pdf.debug_file_list}，請檢查檔案名稱是否合規定'
            send_msg_to_UI(msg)
            return 0
        
        pdf.merge_and_getpage()
        if len(pdf.debug_title_list) != 0:
            print('debug_title_list', pdf.debug_title_list)
            msg = f'WORNING! 第一、二大項有標題未被找到，標題: {pdf.debug_title_list[0]}，請檢查標題是否符合規定'
            send_msg_to_UI(msg)
            return 0
        
        pdf.transfer_outline()
    
        word_outline = pdf.to_word_outline
        word_outline['number'] = number
        word_outline['address'] = address
        word_outline['name'] = name
        print(word_outline)
    except Exception as ex:
        str_ex = str(ex)
        msg = f'ERROR! 錯誤:{str_ex}'
        send_msg_to_UI(msg)
        return 0
    
    else:
        write_word.write_word(folder_path, word_outline)

def create_merger_folder(folder_path):
    now_date = datetime.date.today()
    tmp_folder_path = os.path.join(folder_path, f'{now_date}_merger')
    if not os.path.isdir(tmp_folder_path):
        os.makedirs(tmp_folder_path)


def main(**args):
    number, address, name, folder_path= get_variable_form_UI(**args)
    create_merger_folder(folder_path)
    get_first_page_and_merge_pdf(number, address, name, folder_path)



if "__main__" == __name__:
    get_first_page_and_merge_pdf('V1234', 'lll', 'uuuu', 'C:\\Users\\andy_chien\\Downloads\\整合PDF(all)\\整合前')