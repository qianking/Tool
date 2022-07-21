# reportlab imports for adding footer
from reportlab.pdfgen.canvas import Canvas
W

def add_pdf_footer():

    # Get pages
    reader = PdfReader(/path/to/your/existing/pdf)
    pages = [pagexobj(p) for p in reader.pages]

    # Compose new pdf
    canvas = Canvas(/path/to/your/existing/pdf)

    for page_num, page in enumerate(pages, start=1):
        # Add page
        canvas.setPageSize((page.BBox[2], page.BBox[3]))
        canvas.doForm(makerl(canvas, page))

        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
                
        # draw a footer line
        canvas.setLineWidth(0.5)
        canvas.line(66, 78, page.BBox[2] - 66, 78)

        canvas.setFont('Times-Roman', 8)
                
        # add footer text using x,y coordinates
        canvas.drawString(80, 60, footer_text)
        canvas.restoreState()

        canvas.showPage()

    canvas.save()


