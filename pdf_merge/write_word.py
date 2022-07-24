from docxtpl import DocxTemplate

doc_template_path = r'E:\python\github\Tool\pdf_merge\封面\template.docx'
doc_output_path = r'E:\python\github\Tool\pdf_merge\封面\test_1.docx'
doc = DocxTemplate(doc_template_path)
context = {'number' : "V534"}
doc.render(context)
doc.save(doc_output_path)