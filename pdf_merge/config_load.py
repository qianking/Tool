from copy import deepcopy


config_path = r".\config.ini"
All_Same_Chapter = {}
Stamp_ver_Chapter_1_2_data = {}
Audit_ver_Chapter_1_inner_title = {}
Chapter_number = {}


def load_ini(config_path):
    
    with open(config_path, 'r', encoding="utf-8") as f:
        data = f.read()

    data_list = [i for i in data.split('[') if i.strip() != '']

    for i in data_list[1:]:
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
        
    return All_Same_Chapter, Stamp_ver_Chapter_1_2_data, Audit_ver_Chapter_1_inner_title


    
    


if "__main__" == __name__:
    print(load_ini(config_path))
   

