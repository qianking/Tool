import write_word
import os
import pdf_merger
from glob import glob
import datetime
import win32com.client
import time

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
        return args['number'], args['address'], args['name'], args['folder_path'], args['final_file_name']


def turn_word_to_pdf(input_word):
    wdFormatPDF = 17
    pdf_output_file = input_word.replace('.docx', '.pdf')
    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(input_word)
    doc.SaveAs(pdf_output_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

    return pdf_output_file


def get_first_page_and_merge_pdf(number, address, name, folder_path, output_folder_path):
    pdf = pdf_merger.Merge_Pdf_and_GetOutline(folder_path, output_folder_path)
    pdf.order_file()
    print(pdf.order_dic)
    if len(pdf.debug_file_list) != 0:
        file = '、'.join(pdf.debug_file_list)
        print('debug_file_list:', pdf.debug_file_list)
        msg = f'WORNING! 有檔案未被合併，檔案名 {file}，請檢查檔案名稱是否合規定 \n已停止合併，請重新選擇資料夾'
        #刪除資料夾
        send_msg_to_UI(msg)
        
    time.sleep(1)
    pdf.merge_and_getpage()
    print(pdf.output_merge_pdf_path)
    if len(pdf.debug_title_list) != 0:
        print('debug_title_list', pdf.debug_title_list)
        msg = f'WORNING! 第一、二大項有標題未被找到，標題: {pdf.debug_title_list[0]}，請檢查標題是否符合規定 \n已停止合併，請重新選擇資料夾'
        send_msg_to_UI(msg)
        
    pdf.transfer_outline()
    word_outline = pdf.to_word_outline
    word_outline['number'] = number
    word_outline['address'] = address
    word_outline['name'] = name
    print(word_outline)
    doc_output_path = write_word.write_word(output_folder_path, word_outline)

    return doc_output_path ,pdf.output_merge_pdf_path


def create_merger_folder(folder_path):
    now_date = datetime.date.today()
    tmp_folder_path = os.path.join(folder_path, f'{now_date}_merger')
    if not os.path.isdir(tmp_folder_path):
        os.makedirs(tmp_folder_path)
    return tmp_folder_path


def main(**args):
    try:
        number, address, name, folder_path, final_file_name= get_variable_form_UI(**args)
        start_time = time.time()
        send_msg_to_UI('合併開始...')
        output_folder_path = create_merger_folder(folder_path)
        doc_output_path, output_merge_pdf_path = get_first_page_and_merge_pdf(number, address, name, folder_path, output_folder_path)
        send_msg_to_UI('生成合併pdf檔和封面word檔')
        first_page_pdf_path = turn_word_to_pdf(doc_output_path)
        send_msg_to_UI('生成封面pdf檔')
        final_path = pdf_merger.Merge_Final_PDF(first_page_pdf_path, output_merge_pdf_path, number, final_file_name)
    except Exception as ex:
        str_ex = str(ex)
        print(str_ex)
        msg = f'ERROR! 錯誤 : {str_ex}'
        send_msg_to_UI(msg)
        return 0
    else:
        end_time = time.time()
        cost_time = str(end_time- start_time)
        cost_time = cost_time.split('.')[0]
        msg = f'合併完成!\n生成路徑 : {final_path}\nCost : {cost_time} s'
        send_msg_to_UI(msg)



if "__main__" == __name__:
    turn_word_to_pdf(r'D:\download\整合PDF(all)\整合前\2022-07-26_merger\2022-07-26_frist_page.docx')