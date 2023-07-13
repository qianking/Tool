import fitz
import re

input_path = r"C:\Users\andy_chien\Downloads\555\555\555.pdf"


def remove_page_number(input_path):
    output_path = f"{input_path.split('.')[0]}_no_page.pdf"
    pattern = re.compile(r"(p.\d)")

    doc = fitz.open(input_path)

    page_num = Page.number
        
    for i in range(12):
        page = doc.load_page(i)
        
        ful_txt = page.get_text("words")
        last_txt = ful_txt[-1]
        for txt in last_txt:
            find = pattern.findall(str(txt))
            if len(find):
                draft = page.search_for(find[0])
                for rect in draft:
                    page.add_redact_annot(rect)
                    page.apply_redactions()
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                break
    
    doc.save(output_path, garbage=3, deflate=True)
    return output_path
