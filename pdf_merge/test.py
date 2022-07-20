from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

path_home=r'D:\download\整合PDF\整合前\02_V534_(111.04.13)_地震風力整合大全(100年)_110.12.31_Locked.pdf'
pdf = SimpleDocTemplate(path_home)
flow_obj = []
styles = getSampleStyleSheet()

def gonumpage(flowdoc, pdf):
    s = flowdoc.getPageNumber()
    s = str(s)
    flowdoc.drawCentredString(300, 10, s)
    flowdoc.saveState()

for i in range(1, 10):
    flow_obj.append(PageBreak())

pdf.build(flow_obj, onFirstPage=gonumpage, onLaterPages=gonumpage)


