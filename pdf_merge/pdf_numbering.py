from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

path = r'C:\Users\andy_chien\Downloads\PDF整合\整合前\03_02_V534_BF_new_剪力牆設計_404-100(耐震)_X向_110.10.20.pdf'
outputFile = r'C:\Users\andy_chien\Downloads\PDF整合\整合前\Test_1.pdf'

def create_page_pdf(num, tmp, page_middle_position):
    c = canvas.Canvas(tmp)
    for i in range(1, num+1):
        c.drawString((page_middle_position[i-1]), 20, str(i))
        #c.setFont()
        c.showPage()
    c.save()

def add_page_numbers(pdf_path):
    tmp_pdf = "__tmp.pdf"

    output = PdfFileWriter()
    with open(pdf_path, 'rb') as f:
        input_pdf = PdfFileReader(f, strict = False)
        page_numbers = input_pdf.getNumPages()

        page_middle_position = get_page_size(input_pdf, page_numbers)
        create_page_pdf(page_numbers, tmp_pdf, page_middle_position)

        with open(tmp_pdf, 'rb') as ftmp:
            numberPDF = PdfFileReader(ftmp)
            for p in range(page_numbers):
                page = input_pdf.getPage(p)
                numberLayer = numberPDF.getPage(p)

                page.mergePage(numberLayer)
                output.addPage(page)

            if output.getNumPages():
                with open(outputFile, 'wb') as f:
                    output.write(f)
        os.remove(tmp_pdf)


def get_page_size(input_pdf, page_numbers):
    page_middle_position = []

    for i in range(page_numbers):
        width = float(input_pdf.pages[i].mediabox.getWidth())
        page_middle_position.append(width/2)
    
    print(page_middle_position)
    return page_middle_position



if "__main__" == __name__:
    add_page_numbers(path)
    #get_page_size(path)
