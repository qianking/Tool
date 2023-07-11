from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

input_path = r'C:\Users\andy_chien\Downloads\弱\V600_弱層檢核\OUTPUT\VPDATXE.TXT'
out_path = r'C:\Users\andy_chien\Downloads\弱\V600_弱層檢核\OUTPUT\output.xlsx'
out_pdf_path = r'D:\Qian\弱\V600_弱層檢核\OUTPUT\output.pdf'
origin = r'D:\Qian\弱\弱層說明頁.pdf'
new = r'D:\Qian\弱\iiii.pdf'

    
# PDFs to merge
pdf_files = [r'E:\python\github\Tool\LFS\資料\弱層說明頁.pdf']

# Create a PdfFileWriter object
pdf_writer = PdfFileWriter()

file_merger = PdfFileMerger()
for file_path in pdf_files:
    pdf_reader = PdfFileReader(file_path, "rb")
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

# Path to output file
out_path = r'E:\python\github\Tool\LFS\資料\new.pdf'

# Write to the output file
with open(out_path, 'wb') as out_file:
    pdf_writer.write(out_file)