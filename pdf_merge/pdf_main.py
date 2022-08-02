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
    pdf_data['number'] = basic_data[1]
    pdf_data['address'] = basic_data[2]
    pdf_data['name'] = basic_data[3]
    pdf_data['input_folder_path'] = basic_data[4]
    pdf_data['file_name'] = basic_data[5]
    special_pdf_data = special_data
    if len(special_data) != 0:
        self = special_data['self']
        status = special_data['status']


def turn_word_to_pdf(input_word_path):
    wdFormatPDF = 17
    pdf_output_file = input_word_path.replace('.docx', '.pdf')
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(input_word_path)
    doc.SaveAs(pdf_output_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
    return pdf_output_file


def create_merger_folder():
    now_date = datetime.date.today()
    tmp_file_folder_path = os.path.join(pdf_data['input_folder_path'], f'{now_date}_merger')
    if not os.path.isdir(tmp_file_folder_path):
        os.makedirs(tmp_file_folder_path)
    pdf_data['tmp_file_folder_path'] = tmp_file_folder_path


def get_first_page_and_merge_pdf():
    pdf = merger.Merge_Pdf_and_GetOutline(pdf_data['select_stytle'], pdf_data['input_folder_path'], pdf_data['tmp_file_folder_path'])
    pdf.create_order_dic()
    pdf.find_special_chapter_file()
    pdf.find_same_chapter_file()
    pdf.order_same_chpater()
    pdf.find_special_chapter_page()
    pdf.add_same_and_special_chapter()
    time.sleep(1)
    pdf.merge_all_pdf()
    pdf.transfer_to_word_stytle() 
    output_merge_pdf_path = pdf.output_merge_pdf_path
    word_outline_data = pdf.to_word_outline
        
    word_outline_data['number'] = pdf_data['number']
    word_outline_data['address'] = pdf_data['address']
    word_outline_data['name'] = pdf_data['name']
    if pdf_data['select_stytle'] == '核章版':
        word_outline_data['outline_title'] = special_pdf_data['Audit_selection']
    doc_output_path = word_pdf.write_outline_word(pdf_data['select_stytle'], pdf_data['tmp_file_folder_path'], word_outline_data)
    
    return doc_output_path ,output_merge_pdf_path


def main(basic_data, special_data):
    try:
        start_time = time.time()
        get_variable_form_UI(basic_data, special_data)
        send_msg_to_UI('合併開始...')
        create_merger_folder()
        doc_output_path, output_merge_pdf_path = get_first_page_and_merge_pdf()
        send_msg_to_UI('生成合併pdf檔和封面word檔')
        time.sleep(1)
        outline_pdf_path = turn_word_to_pdf(doc_output_path)
        send_msg_to_UI('生成封面pdf檔')
        time.sleep(1)
        final_path = merger.Merge_Final_PDF(outline_pdf_path, output_merge_pdf_path, pdf_data['number'], pdf_data['file_name'])
        
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
    turn_word_to_pdf(r'D:\download\整合PDF(all)\整合前\2022-07-26_merger\2022-07-26_frist_page.docx')