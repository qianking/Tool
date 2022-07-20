import os
from glob import glob
from PyPDF2 import *
from fpdf import FPDF



class NumberPDF(FPDF):
    def __init__(self, numberofpage):
        super(NumberPDF, self).__init__()
        self.numberofpage = numberofpage

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'{self.page_no()}', 0, 0, 'C')

path = r'C:\Users\andy_chien\Downloads\PDF整合\整合前\03_02_V534_BF_new_剪力牆設計_404-100(耐震)_X向_110.10.20.pdf'

inputFile = PdfFileReader(path)
outputFile = r'C:\Users\andy_chien\Downloads\PDF整合\整合前\Test_2.pdf'
print(inputFile.getNumPages())
tempNumFile = NumberPDF(inputFile.getNumPages())
for pages in range(inputFile.getNumPages()):
    tempNumFile.add_page()

tempNumFile.output('tempNumbering.pdf')

mergeFile = PdfFileReader('tempNumbering.pdf')

mergeWriter = PdfFileWriter()

for x, pages in enumerate(mergeFile.pages):
    inputPage = inputFile.getPage(x)
    inputPage.mergePage(pages)
    mergeWriter.addPage(inputPage)

os.remove('tempNumbering.pdf')

with open(outputFile, 'wb') as fh:
    mergeWriter.write(fh)




''' for pdf in pdf_list:
    merger.append(open(pdf, 'rb'))

output_file = os.path.join(path, 'result.pdf')
with open(output_file, 'wb') as p:
    merger.write(p) '''