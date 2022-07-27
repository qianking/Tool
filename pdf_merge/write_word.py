from docxtpl import DocxTemplate
import datetime
import os

outline_template_path = r'.\cover\outline_template.docx'
cover_template_path = r'.\cover\cover_template.docx'
#doc_output_path = r'C:\封面\test_1.docx'
""" context = {
        'title_1': [
            {'title': '1-1~1-10 設計概要說明', 'page': 1}, 
            {'title': '1-11 建築物重量計算', 'page': 7}, 
            {'title': '1-12 動力分析週期', 'page': 11}, 
            {'title': '1-13 振態說明', 'page': 13}, 
            {'title': '1-14 剛性隔板質心及剛心', 'page': 15}
            ], 
        'title_2': [
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
            ],
        'cover_3': 44, 
        'title_3': [
            {'title': '軟層檢核', 'page': 45}, 
            {'title': '剪力牆設計', 'page': 47}, 
            {'title': '一樓樓版剪力傳遞', 'page': 53}, 
            {'title': '梁上柱檢核', 'page': 57}, 
            {'title': '梁柱韌性與扭力檢核', 'page': 59}, 
            {'title': '極限層剪力檢核', 'page': 69}, 
            {'title': '上浮力檢核', 'page': 71}, 
            {'title': '地下室外牆設計', 'page': 72}, 
            {'title': '無梁版檢核', 'page': 75}, 
            {'title': '基礎設計', 'page': 93}], 
        'cover_4': 99, 
        'title_4': [], 
        'cover_5': 117, 
        'title_5': [
            {'title': '意見回覆', 'page': 118}
            ], 
        'cover_6': 130, 
        'title_6': [
            {'title': '大梁', 'page': 131}
            ]
        } """

context_cover = {'chapter' : '三',
                    'title': '結構設計檢核'

}
def output_path(folder_path):
    now_date = datetime.date.today()
    file_name = f'{now_date}_frist_page.docx'
    doc_output_path = os.path.join(folder_path, file_name)
    return doc_output_path

def write_word(folder_path, context):
    doc_output_path = output_path(folder_path)
    doc = DocxTemplate(outline_template_path)
    doc.render(context)
    doc.save(doc_output_path)
    return doc_output_path


def write_cover_word(folder_path, context):
    doc_output_path = output_path(folder_path)
    doc = DocxTemplate(cover_template_path)
    doc.render(context)
    doc.save(doc_output_path)
    return doc_output_path


if "__main__" == __name__:
    write_cover_word(r'E:\python\github\Tool\pdf_merge\整合PDF(all)\cover', context_cover)