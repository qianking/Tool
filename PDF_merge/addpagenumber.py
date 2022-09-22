from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pagelabels import PageLabels, PageLabelScheme
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import sys
import os


input_file = r'E:\python\virtualenv\Tool\PDF_merger\整合PDF(all)\整合前\核章版 多\2022-08-17_merger\first_chapter_pdf.pdf'
output_file = r'E:\python\virtualenv\Tool\PDF_merger\整合PDF(all)\整合前\核章版 多\2022-08-17_merger\first_chapter_pages.pdf'


reader = PdfReader(input_file)
pages = [pagexobj(p) for p in reader.pages]

canvas = Canvas(output_file)

for page_num, page in enumerate(pages, start=1):
    canvas.doForm(makerl(canvas, page))

    footer_text = f"{page_num}"
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFont('Times-Roman', 12)
    canvas.drawString(290, 10, footer_text)
    canvas.restoreState()
    canvas.showPage()

canvas.save()


