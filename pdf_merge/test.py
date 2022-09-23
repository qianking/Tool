from dataclasses import replace
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject


input_path = r'C:\Users\andy_chien\Downloads\555\555\555.pdf'
out = r'C:\Users\andy_chien\Downloads\整合PDF(all)\整合前\第一次意見回覆_text.pdf'

''' PdfReader = PdfFileReader(input_path)
total_page = PdfReader.getNumPages()

Page_n = PdfReader.getPage(1)
txt = Page_n.extractText()

txt = txt.replace('p.1', ' ')
print(txt)

Page_n = PdfReader.getPage(1)
txt = Page_n.extractText()
print(txt) '''


''' out_put = PdfFileWriter()
out_put.addPage(Page_n)
with open(out, 'wb') as f:
    out_put.write(f)
 '''



replacements = [
    ("p.1", " 555")
]

pdf = PdfFileReader(input_path).getPage(1)
print(pdf)
writer = PdfFileWriter() 

print(pdf.getContents())
contents = pdf.getContents()    .getData()
for (a,b) in replacements:
    contents = contents.replace(a.encode('utf-8'), b.encode('utf-8'))
page.getContents().setData(contents)
writer.addPage(page)
    
with open(out, "wb") as f:
     writer.write(f)
