from docxtpl import DocxTemplate
import datetime
import os
import comtypes.client

Audit_outline_template_path = r'C:\Users\andy_chien\Downloads\整合PDF(all)\cover\Audit_outline_template.docx'
Stamp_outline_template_path = r'C:\Users\andy_chien\Downloads\整合PDF(all)\cover\Stamp_outline_template.docx'
cover_template_path = r'C:\Users\andy_chien\Downloads\整合PDF(all)\cover\cover_template.docx'
#doc_output_path = r'C:\封面\test_1.docx'
context = {
        'title_special': [
            {'big_title':'一、結構設計概要說明', 
                'inner_title': [
                    {'title': '1-1~1-10 設計概要說明', 'page': 1}, 
                    {'title': '1-11 建築物重量計算', 'page': 7}, 
                    {'title': '1-12 動力分析週期', 'page': 11}, 
                    {'title': '1-13 振態說明', 'page': 13}, 
                    {'title': '1-14 剛性隔板質心及剛心', 'page': 15}
                ]}, 
            {'big_title': '二、地震力與風力計算', 
                'inner_title': [
                {'title': '2-1 建築物設計地震力計算', 'page': 16}, 
                {'title': '2-2 垂直地震力計算', 'page': 18}, 
                {'title': '2-3 建築物地震力之豎向分配', 'page': 19}, 
                {'title': '2-4 動力反應譜分析調整放大係數', 'page': 23}, 
                {'title': '2.5 動力分析樓層剪力', 'page': 24}, 
                {'title': '2.6 動力分析質心位移', 'page': 27}, 
                {'title': '2.7 動力分析層間變位角', 'page': 28}, 
                {'title': '2.8 意外扭矩放大係數計算', 'page': 31}, 
                {'title': '2-9 碰撞間隔及層間變位角計算', 'page': 32}, 
                {'title': '2-10 風力計算', 'page': 34}, 
                ]}],
        'title_same':[
            {'big_title':'三、結構設計檢核', 'page': 44,
                'inner_title': [
                    {'title': '軟層檢核', 'page': 45}, 
                    {'title': '剪力牆設計', 'page': 47}, 
                    {'title': '一樓樓版剪力傳遞', 'page': 53}, 
                    {'title': '梁上柱檢核', 'page': 57}, 
                    {'title': '梁柱韌性與扭力檢核', 'page': 59}, 
                    {'title': '極限層剪力檢核', 'page': 69}, 
                    {'title': '上浮力檢核', 'page': 71}, 
                    {'title': '地下室外牆設計', 'page': 72}, 
                    {'title': '無梁版檢核', 'page': 75}, 
                    {'title': '基礎設計', 'page': 93}
                ]},
            {'big_title':'四、開挖設計', 'page': 99, 
                'inner_title': []}], 
        }

''' context_cover = {'title_1_1' : '1-1~1-10設計概要說',
                'data' : [
                    {'title_1': 'A棟 :', 'title_2' : 
                                            [{'title_3': '1-11重量計算', 'page' : '7'},
                                            {'title_3': '1-12動力分析週期及振態參與質量', 'page' : '9'},
                                            {'title_3': '1-13振態說明', 'page' : '11'},
                                            {'title_3': '1-14剛性隔板質心及剛心', 'page' : '13'},],
                                            'title_4' :
                                            [{'title_5': '2-1建築物設計地震力計算', 'page' : '14'},
                                            {'title_5': '2-2垂直地震力計算', 'page' : '16'},
                                            {'title_5': '2-3建築物地震力之豎向分配', 'page' : '17'},
                                            {'title_5': '2-4動力反應譜分析調整放大係數', 'page' : '21'},]}, 
                    {'title_1': 'B棟 :', 'title_2' : 
                                            [{'title_3': '1-11重量計算', 'page' : '40'},
                                            {'title_3': '1-12動力分析週期及振態參與質量', 'page' : '42'},
                                            {'title_3': '1-13振態說明', 'page' : '44'},
                                            {'title_3': '1-14剛性隔板質心及剛心', 'page' : '46'},],
                                            'title_4' :
                                            [{'title_5': '2-1建築物設計地震力計算', 'page' : '47'},
                                            {'title_5': '2-2垂直地震力計算', 'page' : '49'},
                                            {'title_5': '2-3建築物地震力之豎向分配', 'page' : '50'},
                                            {'title_5': '2-4動力反應譜分析調整放大係數', 'page' : '52'},]}]} '''
                 

template = {'核章版': Stamp_outline_template_path,
            '外審版' : Audit_outline_template_path}

def output_path(output_folder_path, file_name):
    out_put_file_name = f'{file_name}.docx'
    doc_output_path = os.path.join(output_folder_path, out_put_file_name)
    return doc_output_path

def write_outline_word(stytle, folder_path, file_name, context):
    doc_output_path = output_path(folder_path, file_name)
    doc = DocxTemplate(template[stytle])
    doc.render(context)
    doc.save(doc_output_path)
    return doc_output_path


def write_cover_word(output_folder_path, file_name, context):
    doc_output_path = output_path(output_folder_path, file_name)
    doc = DocxTemplate(cover_template_path)
    doc.render(context)
    doc.save(doc_output_path)
    return doc_output_path


def turn_word_to_pdf(input_word_path):
    wdFormatPDF = 17
    pdf_output_file = input_word_path.replace('.docx', '.pdf')
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(input_word_path)
    doc.SaveAs(pdf_output_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

    return pdf_output_file


if "__main__" == __name__:
    write_outline_word(r'E:\python\github\Tool\pdf_merge\整合PDF(all)\cover', 'test', context)