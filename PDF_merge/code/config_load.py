from copy import deepcopy
import re

config_path = r".\config.ini"
All_Same_Chapter = {}
Stamp_ver_Chapter_1_2_data = {}
Audit_ver_Chapter_1_inner_title = {}
Chapter_number = {}


""" def load_ini(config_path):
    
    with open(config_path, 'r', encoding="utf-8") as f:
        data = f.read()
    print(repr(data))
    data_list = [i for i in data.split('[') if i.strip() != '']

    for i in data_list:
        session_name = i[:i.index(']')]
        tmp_data = [i.strip() for i in i[i.index(']'):].split('\n\n')[1:] if i.strip() != '']
        for j in tmp_data:
            tmp_chapter_data = [i.strip() for i in j.split('\n') if i.strip() != '']
            chapter = int(tmp_chapter_data[0].split('=')[1].strip())
            tmp_chapter_data.pop(0)
            title = tmp_chapter_data[0].split('=')[1].strip()
            tmp_chapter_data.pop(0)   
            tmp_list = list() 
            for i, num in enumerate(tmp_chapter_data, 1):
                if i != int(num.split('=')[0].strip()):
                    print('config錯誤')
                    return 0
                else:
                    tmp_list.append(num.split('=')[1].strip())
            if not len(tmp_list):
                tmp_list = None

            if session_name == '共同章節':
                All_Same_Chapter[chapter] = {'title': title, 'inner_title_and_file_name': deepcopy(tmp_list)}
            if session_name == '核章版專屬章節':
                Stamp_ver_Chapter_1_2_data[chapter] = {'title': title}
            if session_name == '外審版專屬章節':
                Audit_ver_Chapter_1_inner_title[chapter] = {'title': title}
        
    return All_Same_Chapter, Stamp_ver_Chapter_1_2_data, Audit_ver_Chapter_1_inner_title """

def load_ini(config_path):
    with open(config_path, 'r', encoding="utf-8") as f:
        data = f.read()

    data_list = [i for i in data.split('\n\n') if i.strip() != '']
    for data in data_list:
        data_de = [i for i in data.split('\n') if i.strip() != '']
        tmp_list = list() 
        for dd in data_de:
            if data.startswith('#'):
                flage = True
                continue
            if dd.strip().startswith('[') and dd.strip().endswith(']'):
                session_name = dd.strip()[1:-1]
                flage = True
                break

            if dd.strip().startswith('chapter'):
                chapter = int(dd.split('=')[1].strip())
            
            elif dd.strip().startswith('title'):
                title = dd.split('=')[1].strip()
            
            else:
                tmp_list.append(dd.split('=')[1].strip())
        
        if flage:
            flage = False
            continue
        if session_name == '共同章節':
            if not len(tmp_list):
                tmp_list = None
            All_Same_Chapter[chapter] = {'title': title, 'inner_title_and_file_name': deepcopy(tmp_list)}
        if session_name == '核章版專屬章節':
            Stamp_ver_Chapter_1_2_data[chapter] = {'title': title}
        if session_name == '外審版專屬章節':
            Audit_ver_Chapter_1_inner_title[chapter] = {'title': title}

    """ print(All_Same_Chapter)
    print(Stamp_ver_Chapter_1_2_data)
    print(Audit_ver_Chapter_1_inner_title) """

    return All_Same_Chapter, Stamp_ver_Chapter_1_2_data, Audit_ver_Chapter_1_inner_title       
    
    
        
        

        


    
"""   
if session_name == '共同章節':
    All_Same_Chapter[chapter] = {'title': title, 'inner_title_and_file_name': deepcopy(tmp_list)}
if session_name == '核章版專屬章節':
    Stamp_ver_Chapter_1_2_data[chapter] = {'title': title}
if session_name == '外審版專屬章節':
    Audit_ver_Chapter_1_inner_title[chapter] = {'title': title} """

if "__main__" == __name__:
    config_path = r"E:\python\github\Tool\PDF_merge\config.ini"
    load_ini(config_path)
   

