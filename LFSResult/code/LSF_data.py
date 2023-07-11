import os 
import sys
import re
from copy import deepcopy

input_X_shear = r'E:\python\github\Tool\LFSResult\資料\弱層檢核\OUTPUT\V534VPDATXE_NSW.txt'
input_X = r'E:\python\github\Tool\LFSResult\資料\弱層檢核\OUTPUT\V534VPDATXE.txt'
input_Y_shear = r'E:\python\github\Tool\LFSResult\資料\弱層檢核\OUTPUT\V534VPDATYE_NSW.txt'
input_Y = r'E:\python\github\Tool\LFSResult\資料\弱層檢核\OUTPUT\V534VPDATYE.txt'
adjust = True
level = '1MF'
H = 5.45


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

def datatransfer():
    with open(input_X_shear, 'r') as f:
        X_shear= f.read()

    with open(input_X, 'r') as f:
        X= f.read()

    with open(input_Y_shear, 'r') as f:
        Y_shear= f.read()

    with open(input_Y, 'r') as f:
        Y= f.read()

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

    #X計算
    X_floor_list = list()
    X_VPXw = list()

    for i, x in enumerate(X_shear_all_data):
        X_floor_list.append(x[0])
        a = CustomList(x)
        b = CustomList(X_all_data[i])
        a_data = a.get(X_shear_title['VPX(t)'], "")
        b_data = b.get(X_shear_title['VPX(t)'], "")
        if a_data == "" or b_data == "":
            X_VPXw.append("")
        else:
            X_VPXw.append(a_data - b_data)

    #如果有需要調整的樓層    
    if adjust:
        adjust_INDEX = X_floor_list.index(level)
        FirstF_INDEX = X_floor_list.index('1F')

        adjust_MPT = X_shear_all_data[adjust_INDEX][X_shear_title['MPT(t-m)']]
        adjust_MPB = X_shear_all_data[-1][X_shear_title['MPB(t-m)']]
        adjust_VPX = round(((adjust_MPT + adjust_MPB)/H)+ X_VPXw[FirstF_INDEX], 2)
        adjust_VEX = X_shear_all_data[-1][X_shear_title['VEX(t)']]
        adjust_VPVE = round(adjust_VPX/adjust_VEX, 2)
        adjust_Bx = round(adjust_VPVE/X_shear_all_data[adjust_INDEX-1][X_shear_title['VP/VE']], 2)
        adjust_08Bx= "OK" if adjust_Bx >0.8 else "NG"
        
        new_FirstF_data = ['1F', H, adjust_MPT, adjust_MPB, adjust_VPX, adjust_VEX, adjust_VPVE, adjust_Bx, adjust_08Bx]
        X_shear_all_data[FirstF_INDEX] = new_FirstF_data
        X_shear_all_data.remove(X_shear_all_data[adjust_INDEX])
    
    
    
    #Y計算
    Y_floor_list = list()
    Y_VPXw = list()

    for i, y in enumerate(Y_shear_all_data):
        Y_floor_list.append(y[0])
        a = CustomList(y)
        b = CustomList(Y_all_data[i])
        a_data = a.get(Y_shear_title['VPY(t)'], "")
        b_data = b.get(Y_shear_title['VPY(t)'], "")
        if a_data == "" or b_data == "":
            Y_VPXw.append("")
        else:
            Y_VPXw.append(a_data - b_data)

    #如果有需要調整的樓層    
    if adjust:
        adjust_INDEX = Y_floor_list.index(level)
        FirstF_INDEX = Y_floor_list.index('1F')

        adjust_MPT = Y_shear_all_data[adjust_INDEX][Y_shear_title['MPT(t-m)']]
        adjust_MPB = Y_shear_all_data[-1][Y_shear_title['MPB(t-m)']]
        adjust_VPX = round(((adjust_MPT + adjust_MPB)/H) + Y_VPXw[FirstF_INDEX], 2)
        adjust_VEX = Y_shear_all_data[-1][Y_shear_title['VEY(t)']]
        adjust_VPVE = round(adjust_VPX/adjust_VEX, 2)
        adjust_Bx = round(adjust_VPVE/Y_shear_all_data[adjust_INDEX-1][Y_shear_title['VP/VE']], 2)
        adjust_08Bx= "OK" if adjust_Bx >0.8 else "NG"
        
        
        new_FirstF_data = ['1F', H, adjust_MPT, adjust_MPB, adjust_VPX, adjust_VEX, adjust_VPVE, adjust_Bx, adjust_08Bx]
        Y_shear_all_data[FirstF_INDEX] = new_FirstF_data
        Y_shear_all_data.remove(Y_shear_all_data[adjust_INDEX])



        
    
        
        
    



if __name__ == "__main__":
    datatransfer() 

    

