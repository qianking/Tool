import os
import win32com.client
import win32gui
import win32con
from PyPDF2 import PdfFileReader, PdfFileWriter

excel_output_path = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT\report.xlsx'
pdf_output_path = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT'

pdf_list = [r"C:\Users\andy_chien\Downloads\資料\弱層說明頁.pdf"]
final_pdf = r"C:\Users\andy_chien\Downloads\資料\REPORT.pdf"

def Transfer_PDF(pdf_list, excel_input, pdf_out):

    excel = win32com.client.Dispatch("Excel.Application")

    #隱藏將要開啟的excel檔案
    hwnd = win32gui.FindWindow(None, "report")  
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # 打开Excel文件
    wb = excel.Workbooks.Open(excel_input)

    # 遍历每个工作表
    for ws in wb.Worksheets:

        # 调整页面设置以适应所有列
        ws.PageSetup.Zoom = False
        ws.PageSetup.FitToPagesWide = 1  # 所有列适应在一个页面宽
        ws.PageSetup.FitToPagesTall = 1  # 页面的高度可以是任意的

        """ ws.PageSetup.LeftMargin = 25
        ws.PageSetup.RightMargin = 25
        ws.PageSetup.TopMargin = 50
        ws.PageSetup.BottomMargin = 50 """

        # 導出該工作表為 PDF
        pdf_out_path = os.path.join(pdf_out, f"{ws.Name}.pdf")       
        ws.ExportAsFixedFormat(0, pdf_out_path)
        pdf_list.append(pdf_out_path)
    # 关闭Excel文件
    wb.Close()

    return pdf_list

def PDF_Merge(pdf_list, final_pdf):

    pdf_writer = PdfFileWriter()

    for file_path in pdf_list:
        pdf_reader = PdfFileReader(file_path, "rb")
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    
    with open(final_pdf, 'wb') as out_file:
        pdf_writer.write(out_file)

if __name__ == "__main__":
    pdf_list =Transfer_PDF(pdf_list, excel_output_path, pdf_output_path)
    PDF_Merge(pdf_list, final_pdf)