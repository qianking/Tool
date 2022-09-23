from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
from pdfrw import PdfReader, PageMerge

input_path = r'C:\Users\andy_chien\Downloads\整合PDF(all)_2\2022-09-23_merge.pdf'

"""
如要使用請先去  \Python39\lib\site-packages\reportlab\pdfbase\pdfdoc.py 裡面的 line 54 改成 
def pdfdocEnc(x):
    try:
        return x.encode('extpdfdoc') if isinstance(x,str) else x  
    except:
        return x.encode('utf-8') if isinstance(x,str) else x 
"""

def add_page_number(input_path):
    page_data_dic = {}
    reader = PdfReader(input_path ,decompress=False)
    for num, p in enumerate(reader.pages, start=1):
        tmp_size = p.MediaBox
        tmp_data = p.Rotate      #取得該頁是否有選轉過，旋轉幾度
        if p.Rotate:
            tmp_data = int(p.Rotate)
        page_data_dic[num] = {'rotate': tmp_data, 'size': (float(tmp_size[2]), float(tmp_size[3]))}

    output_file = f"{input_path.split('.')[0]}_pages.pdf"
    canvas = Canvas(output_file)

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        p = pagexobj(PageMerge().add(page).render())   #將這頁以浮水印的方式存起來
        page_size = page_data_dic[i+1]['size']  #得到該頁的頁面大小
        if page_data_dic[i+1]['rotate'] == 90:
            page_size = (page_size[1], page_size[0])  #如果有旋轉過，那就將該頁的高和寬交換
        canvas.setPageSize([page_size[0], page_size[1]])  #設定該頁的紙張大小
        canvas.doForm(makerl(canvas, p))  #將原PDF裡面的該頁面複製到新的PDF裡
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setFont('Times-Roman', 12)  #設定頁碼格式
        canvas.drawString(page_size[0]/2, 25, f"p.{i+1}")
        canvas.restoreState()
        canvas.showPage()
    canvas.save() 

    return output_file

if "__main__" == __name__:
    add_page_number(input_path)
