from LSF_DataTransfer import DataTransfer
from LSF_ToExcel import Transfer_Excel
from LSF_ToPDF import Transfer_PDF

root_path = r"C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT"

data = {'input_X_shear':rf'{root_path}\V534VPDATXE_NSW.txt',
        'input_X':rf'{root_path}\V534VPDATXE.txt',
        'input_Y_shear':rf'{root_path}\V534VPDATYE_NSW.txt',
        'input_Y':rf'{root_path}\V534VPDATYE.txt',
        'adjust':True,
        'level':'1MF',
        'H':5.45,}

excel_output_path = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT\report.xlsx'
pdf_output_file = r'C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT'



def Main():
    X_shear_data, Y_shear_data = DataTransfer(data)
    Transfer_Excel(X_shear_data, Y_shear_data, excel_output_path)
    pdf_list = Transfer_PDF(excel_output_path,pdf_output_file)
    print(pdf_list)




if __name__ == "__main__":
    Main()