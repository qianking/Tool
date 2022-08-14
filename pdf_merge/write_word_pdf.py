from docxtpl import DocxTemplate
import datetime
import os
import comtypes.client

root_path = r'E:\python\github\Tool\pdf_merge\整合PDF(all)\cover'
Audit_outline_template_path = os.path.join(root_path, 'Audit_outline_template.docx')
Stamp_single_outline_template_path = os.path.join(root_path, 'Stamp_single_outline_template.docx')
Stamp_multi_outline_template_path = os.path.join(root_path, 'Stamp_multi_outline_template.docx')
cover_template_path = os.path.join(root_path, 'cover_template.docx')
#doc_output_path = r'C:\封面\test_1.docx'
""" context = {
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
        } """

"""context = {'title_special_1' : 
                    [{'big_title':'一、結構設計概要說明',
                        'inner_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3},]}],
            'title_special_2' :
                    [{'build_titie':'A棟',
                        'inner_1_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}],
                    'big_title':'二、地震力與風力計算',
                        'inner_2_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}]},
                    {'build_titie':'B棟',
                        'inner_1_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}],
                    'big_title':'二、地震力與風力計算',
                        'inner_2_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}]},
                    {'build_titie':'C棟',
                        'inner_1_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}],
                    'big_title':'二、地震力與風力計算',
                        'inner_2_title': [
                            {'title': '1-1 建築概要', 'page': 1},
                            {'title': '1-2 結構系統', 'page': 1},
                            {'title': '1-5 主要材料強度', 'page': 3}]}],
                    
                    }"""
content = {'title_special_1': [
                {'big_title': '一、結構設計概要說明', 
                        'inner_title': [
                            {'title': '1-1 建築概要', 'page': 1}, 
                            {'title': '1-2 結構系統', 'page': 1}, 
                            {'title': '1-3 結構模型示意圖', 'page': 1}, 
                            {'title': '1-4 設計規範', 'page': 3}, 
                            {'title': '1-5 主要材料強度', 'page': 3}, 
                            {'title': '1-6 設計載重', 'page': 3}, 
                            {'title': '1-7 構材尺寸', 'page': 4}, 
                            {'title': '1-8 分析程式', 'page': 4}, 
                            {'title': '1-9 載重組合', 'page': 5}, 
                            {'title': '1-10 地震作用時層間變位檢討', 'page': 6}]}], 
        'title_special_2': [
                {'build_titie': '1棟', 
                        'inner_1_title': [
                            {'title': '1-11 建築物重量計算', 'page': 7}, 
                            {'title': '1-12 動力分析週期', 'page': 11}, 
                            {'title': '1-13 振態說明', 'page': 13}, 
                            {'title': '1-14 剛性隔板質心及剛心', 'page': 15}], 
                'big_title': '二、地震力與風力計算', 
                        'inner_2_title': [
                            {'title': '2-1 建築物設計地震力計算', 'page': 16}, 
                            {'title': '2-2 垂直地震力計算', 'page': 18}, 
                            {'title': '2-3 建築物地震力之豎向分配', 'page': 19}, 
                            {'title': '2-4 動力反應譜分析調整放大係數', 'page': 23}, 
                            {'title': '2-5 動力分析樓層剪力', 'page': 24}, 
                            {'title': '2-6 動力分析質心位移', 'page': 27}, 
                            {'title': '2-7 動力分析層間變位角', 'page': 28}, 
                            {'title': '2-8 意外扭矩放大係數計算', 'page': 31}, 
                            {'title': '2-9 碰撞間隔及層間變位角計算', 'page': 32}, 
                            {'title': '2-10 風力計算', 'page': 34}]}, 
                {'build_titie': '2棟', 
                        'inner_1_title': [
                            {'title': '1-11 建築物重量計算', 'page': 44}, 
                            {'title': '1-12 動力分析週期', 'page': 48}, 
                            {'title': '1-13 振態說明', 'page': 50}, 
                            {'title': '1-14 剛性隔板質心及剛心', 'page': 52}], 
                'big_title': '二、地震力與風力計算', 
                        'inner_2_title': [
                            {'title': '2-1 建築物設計地震力計算', 'page': 53}, 
                            {'title': '2-2 垂直地震力計算', 'page': 55}, 
                            {'title': '2-3 建築物地震力之豎向分配', 'page': 56}, 
                            {'title': '2-4 動力反應譜分析調整放大係數', 'page': 60}, 
                            {'title': '2-5 動力分析樓層剪力', 'page': 61}, 
                            {'title': '2-6 動力分析質心位移', 'page': 64}, 
                            {'title': '2-7 動力分析層間變位角', 'page': 65}, 
                            {'title': '2-8 意外扭矩放大係數計算', 'page': 68}, 
                            {'title': '2-9 碰撞間隔及層間變位角計算', 'page': 69}, 
                            {'title': '2-10 風力計算', 'page': 71}]}, 
                {'build_titie': '3棟', 
                        'inner_1_title': [
                            {'title': '1-11 建築物重量計算', 'page': 81}, 
                            {'title': '1-12 動力分析週期', 'page': 85}, 
                            {'title': '1-13 振態說明', 'page': 87}, 
                            {'title': '1-14 剛性隔板質心及剛心', 'page': 89}], 
                'big_title': '二、地震力與風力計算', 
                        'inner_2_title': [
                            {'title': '2-1 建築物設計地震力計算', 'page': 90}, 
                            {'title': '2-2 垂直地震力計算', 'page': 92}, 
                            {'title': '2-3 建築物地震力之豎向分配', 'page': 93}, 
                            {'title': '2-4 動力反應譜分析調整放大係數', 'page': 97}, 
                            {'title': '2-5 動力分析樓層剪力', 'page': 98}, 
                            {'title': '2-6 動力分析質心位移', 'page': 101}, 
                            {'title': '2-7 動力分析層間變位角', 'page': 102}, 
                            {'title': '2-8 意外扭矩放大係數計算', 'page': 105}, 
                            {'title': '2-9 碰撞間隔及層間變位角計算', 'page': 106}, 
                            {'title': '2-10 風力計算', 'page': 108}]}, 
                {'build_titie': '4棟', 
                        'inner_1_title': [
                            {'title': '1-11 建築物重量計算', 'page': 118}, 
                            {'title': '1-12 動力分析週期', 'page': 122}, 
                            {'title': '1-13 振態說明', 'page': 124}, 
                            {'title': '1-14 剛性隔板質心及剛心', 'page': 126}], 
                'big_title': '二、地震力與風力計算', 
                        'inner_2_title': [
                            {'title': '2-1 建築物設計地震力計算', 'page': 127}, 
                            {'title': '2-2 垂直地震力計算', 'page': 129}, 
                            {'title': '2-3 建築物地震力之豎向分配', 'page': 130}, 
                            {'title': '2-4 動力反應譜分析調整放大係數', 'page': 134}, 
                            {'title': '2-5 動力分析樓層剪力', 'page': 135}, 
                            {'title': '2-6 動力分析質心位移', 'page': 138}, 
                            {'title': '2-7 動力分析層間變位角', 'page': 139}, 
                            {'title': '2-8 意外扭矩放大係數計算', 'page': 142}, 
                            {'title': '2-9 碰撞間隔及層間變位角計算', 'page': 143}, 
                            {'title': '2-10 風力計算', 'page': 145}]}], 
        'title_same': [
                {'big_title': '三、結構設計檢核', 'page': 155, 
                        'inner_title': [
                            {'title': '1.  軟層檢核', 'page': 156}, 
                            {'title': '2.  剪力牆設計', 'page': 158}, 
                            {'title': '3.  一樓樓版剪力傳遞', 'page': 164}, 
                            {'title': '4.  梁上柱檢核', 'page': 168}, 
                            {'title': '5.  梁柱韌性與扭力檢核', 'page': 170}, 
                            {'title': '6.  極限層剪力檢核', 'page': 180}, 
                            {'title': '7.  上浮力檢核', 'page': 182}, 
                            {'title': '8.  地下室外牆設計', 'page': 183}, 
                            {'title': '9.  無梁版檢核', 'page': 186}, 
                            {'title': '10. 基礎設計', 'page': 204}]}, 
                {'big_title': '四、開挖設計', 'page': 210, 
                        'inner_title': []}, 
                {'big_title': '五、結構外審意見回覆', 'page': 228, 
                        'inner_title': [
                            {'title': '1.  第一次意見回覆', 'page': 229}]}, 
                {'big_title': '六、設計分析報表', 'page': 241, 
                        'inner_title': [
                            {'title': '1.  大梁、柱、牆', 'page': 242}]}]}
                 

template = {'Stamp_single': Stamp_single_outline_template_path,
            'Stamp_multi': Stamp_multi_outline_template_path,
            'Audit' : Audit_outline_template_path}

def output_path(output_folder_path, file_name):
    out_put_file_name = f'{file_name}.docx'
    doc_output_path = os.path.join(output_folder_path, out_put_file_name)
    return doc_output_path

def write_outline_word(stytle, folder_path, context, file_name = 'Outline'):
    doc_output_path = output_path(folder_path, file_name)
    doc = DocxTemplate(template[stytle])
    doc.render(context)
    doc.save(doc_output_path)
    return doc_output_path


def write_cover_word(output_folder_path, context, file_name):
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
    write_outline_word('Stamp_multi', r'E:\python\github\Tool\pdf_merge\整合PDF(all)', content)