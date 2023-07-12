
root_path = r"C:\Users\andy_chien\Downloads\資料\弱層檢核\OUTPUT"

data = {'input_X_shear':rf'{root_path}\V534VPDATXE_NSW.txt',
        'input_X':rf'{root_path}\V534VPDATXE.txt',
        'input_Y_shear':rf'{root_path}\V534VPDATYE_NSW.txt',
        'input_Y':rf'{root_path}\V534VPDATYE.txt',
        'adjust':True,
        'level':'1MF',
        'H':5.45,}


class CustomList(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default

def convert_list_number(lst:list):
    new_lst = list()
    for i in lst:
        new_sublst = list()
        for j in i:
            new_sublst.append(convert_to_number(j))
        new_lst.append(new_sublst)
    return new_lst

def convert_to_number(s):
    # 檢查字串是否只包含數字
    if s.isdigit():        
        return int(s)
    # 檢查字串是否為浮點數
    elif s.replace('.', '', 1).isdigit() and s.count('.')<2:
        return float(s)  # 轉換成浮點數
    else:
        return s  # 不轉換

def DataTransfer(data):
    with open(data['input_X_shear'], 'r') as f:
        X_shear= f.read()

    with open(data['input_X'], 'r') as f:
        X= f.read()

    with open(data['input_Y_shear'], 'r') as f:
        Y_shear= f.read()

    with open(data['input_Y'], 'r') as f:
        Y= f.read()

    #region 前處理

    #取得LEVEL後面的所有資料
    #pattern = r'(LEVEL.*)' re.findall(pattern, X_shear, re.DOTALL)
    X_shear_data = X_shear.strip().split("\n")
    X_data = X.strip().split("\n")
    Y_shear_data = Y_shear.strip().split("\n")
    Y_data = Y.strip().split("\n")

    X_shear_data = [a.split() for a in X_shear_data]
    X_data = [a.split() for a in X_data]
    Y_shear_data = [a.split() for a in Y_shear_data]
    Y_data = [a.split() for a in Y_data]

    #檢查資料長度
    if len(X_shear_data) != len(X_data):
        print("X和X剪資料長度不同")
        return 
    if len(Y_shear_data) != len(Y_data):
        print("Y和Y剪資料長度不同")
        return
    
    #將數據都轉換成數字
    X_shear_data = convert_list_number(X_shear_data)
    X_data= convert_list_number(X_data)
    Y_shear_data= convert_list_number(Y_shear_data)
    Y_data= convert_list_number(Y_data)

    #獲得title的每個分別list
    X_shear_title = X_shear_data[2]
    X_title = X_data[2]
    Y_shear_title = Y_shear_data[2]
    Y_title = Y_data[2]
    
    #獲得title名子對應的index的字典
    X_shear_title = {val: i for i, val in enumerate(X_shear_title)}
    X_title = {val: i for i, val in enumerate(X_title)}
    Y_shear_title = {val: i for i, val in enumerate(Y_shear_title)}
    Y_title = {val: i for i, val in enumerate(Y_title)}

    #獲得除了title之外的數據
    X_shear_all_data = X_shear_data[3:]
    X_all_data = X_data[3:]
    Y_shear_all_data = Y_shear_data[3:]
    Y_all_data = Y_data[3:]

    #endregion

    #region X計算
    X_floor_list = list()
    X_VPXw = list()

    len_X = len(X_shear_title)

    for i, x in enumerate(X_shear_all_data):
        X_floor_list.append(x[0])
        a = CustomList(x)
        b = CustomList(X_all_data[i])
        a_data = a.get(X_shear_title['VPX(t)'], "")
        b_data = b.get(X_shear_title['VPX(t)'], "")
        if a_data == "" or b_data == "":
            X_VPXw.append("")
        else:
            X_VPXw.append(round((a_data - b_data), 2))

    #如果有需要調整的樓層    
    if data['adjust']:
        adjust_INDEX = X_floor_list.index(data['level'])
        FirstF_INDEX = X_floor_list.index('1F')

        adjust_MPT = X_shear_all_data[adjust_INDEX][X_shear_title['MPT(t-m)']]
        adjust_MPB = X_shear_all_data[-1][X_shear_title['MPB(t-m)']]
        adjust_VPX = round(((adjust_MPT + adjust_MPB)/data['H']),2)
        adjust_VPXt = round(adjust_VPX + X_VPXw[FirstF_INDEX], 2)
        adjust_VEX = X_shear_all_data[-1][X_shear_title['VEX(t)']]
        adjust_VPVE = round(adjust_VPXt/adjust_VEX, 2)
        adjust_Bx = round(adjust_VPVE/X_shear_all_data[adjust_INDEX-1][X_shear_title['VP/VE']], 2)
        adjust_08Bx= "OK" if adjust_Bx >0.8 else "NG"
        
        new_FirstF_data = ['1F', data['H'], adjust_MPT, adjust_MPB, adjust_VPX, adjust_VEX, adjust_VPVE, adjust_Bx, adjust_08Bx]
        X_shear_all_data[FirstF_INDEX] = new_FirstF_data
        X_shear_all_data.remove(X_shear_all_data[adjust_INDEX])
        X_VPXw.remove(X_VPXw[adjust_INDEX])


    insert_index = X_shear_title['VPX(t)'] + 1  
    for i, datas in enumerate(X_shear_all_data):    
        for _ in range(len_X-len(datas)):  #長度補齊
            datas.append('')

        bx = datas[X_shear_title['Bx']]   #檢查Bx大小
        if bx != '' and bx < 0.8:
            datas[X_shear_title['Bx>0.8']] = "NG"   

        datas.insert(insert_index, X_VPXw[i])  #插入VPXw
 
    X_shear_data[2].insert(insert_index, "VPXw")
    X_shear_data[3:] = X_shear_all_data

    temp_lst = list()
    temp_lst.append("X向")
    for datas in X_shear_data[0]:
        temp_lst.append(datas)
    for _ in range(len(X_shear_data[2])-len(temp_lst)):
        temp_lst.append('')
    X_shear_data[0] = temp_lst

    temp_lst = list()
    temp_lst.append("")    
    for datas in X_shear_data[1]:
        temp_lst.append(datas)
    for _ in range(len(X_shear_data[2])-len(temp_lst)):
        temp_lst.append('')
    X_shear_data[1] = temp_lst  
    #endregion


    #region Y計算
    Y_floor_list = list()
    Y_VPYw = list()

    for i, y in enumerate(Y_shear_all_data):
        Y_floor_list.append(y[0])
        a = CustomList(y)
        b = CustomList(Y_all_data[i])
        a_data = a.get(Y_shear_title['VPY(t)'], "")
        b_data = b.get(Y_shear_title['VPY(t)'], "")
        if a_data == "" or b_data == "":
            Y_VPYw.append("")
        else:
            Y_VPYw.append(round((a_data - b_data), 2))

    #如果有需要調整的樓層    
    if data['adjust']:
        adjust_INDEX = Y_floor_list.index(data['level'])
        FirstF_INDEX = Y_floor_list.index('1F')

        adjust_MPT = Y_shear_all_data[adjust_INDEX][Y_shear_title['MPT(t-m)']]
        adjust_MPB = Y_shear_all_data[-1][Y_shear_title['MPB(t-m)']]
        adjust_VPY = round(((adjust_MPT + adjust_MPB)/data['H']),2)
        adjust_VPYt = round(adjust_VPY + Y_VPYw[FirstF_INDEX], 2)
        adjust_VEY = Y_shear_all_data[-1][Y_shear_title['VEY(t)']]
        adjust_VPVE = round(adjust_VPYt/adjust_VEY, 2)
        adjust_By = round(adjust_VPVE/Y_shear_all_data[adjust_INDEX-1][Y_shear_title['VP/VE']], 2)
        adjust_08By= "OK" if adjust_By >0.8 else "NG"
                
        new_FirstF_data = ['1F', data['H'], adjust_MPT, adjust_MPB, adjust_VPY, adjust_VEY, adjust_VPVE, adjust_By, adjust_08By]
        Y_shear_all_data[FirstF_INDEX] = new_FirstF_data
        Y_shear_all_data.remove(Y_shear_all_data[adjust_INDEX])
        Y_VPYw.remove(Y_VPYw[adjust_INDEX])

    insert_index = Y_shear_title['VPY(t)'] + 1  
    for i, datas in enumerate(Y_shear_all_data):    
        for _ in range(len_X-len(datas)):  #長度補齊
            datas.append('')

        by = datas[Y_shear_title['By']]   #檢查By大小
        if by != '' and by < 0.8:
            datas[Y_shear_title['By>0.8']] = "NG"   

        datas.insert(insert_index, Y_VPYw[i])  #插入VPYw
 
    Y_shear_data[2].insert(insert_index, "VPYw")
    Y_shear_data[3:] = Y_shear_all_data

    temp_lst = list()
    temp_lst.append("Y向")
    for datas in Y_shear_data[0]:
        temp_lst.append(datas)
    for _ in range(len(Y_shear_data[2])-len(temp_lst)):
        temp_lst.append('')
    Y_shear_data[0] = temp_lst

    temp_lst = list()
    temp_lst.append("")    
    for datas in Y_shear_data[1]:
        temp_lst.append(datas)
    for _ in range(len(Y_shear_data[2])-len(temp_lst)):
        temp_lst.append('')
    Y_shear_data[1] = temp_lst 
    #endregion
    
    return X_shear_data, Y_shear_data

    

if __name__ == "__main__":
    DataTransfer(data) 

    

