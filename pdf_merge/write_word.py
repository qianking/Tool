from docxtpl import DocxTemplate

doc_template_path = r'E:\python\github\Tool\pdf_merge\封面\template.docx'
doc_output_path = r'E:\python\github\Tool\pdf_merge\封面\test_1.docx'
doc = DocxTemplate(doc_template_path)
context = {
        
        "data": [

            {'title' : "1-1~1-10設計概要說明"},
            {'title' : "1-11重量計算"}


        ]                 
            
    }

doc.render(context)
doc.save(doc_output_path)