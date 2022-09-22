from copy import deepcopy


config_path = r"D:\Qian\python\GIT\Tool\pdf_merge\config.ini"
All_Same_Chapter = {}
Stamp_ver_Chapter_1_2_data = {}
Audit_ver_Chapter_1_inner_title = {}
Chapter_number = {}


def load_ini(config_path):
    
    with open(config_path, 'r', encoding="utf-8") as f:
        data = f.read()

    data_list = [i for i in data.split('[') if i.strip() != '']
    print(data_list)

    for i in data_list:
        if i[:i.index(']')] == '共同章節':
            tmp_data = [i.strip() for i in i[i.index(']'):].split('\n\n')[1:] if i.strip() != '']
            for j in tmp_data:
                tmp_chapter_data = [i.strip() for i in j.split('\n') if i.strip() != '']
                chapter = tmp_chapter_data[0].split('=')[1].strip()
                tmp_chapter_data.pop(0)
                title = tmp_chapter_data[0].split('=')[1].strip()
                tmp_chapter_data.pop(0)   
                All_Same_Chapter[chapter] = {'title': title}
                tmp_list = list() 
                for i, num in enumerate(tmp_chapter_data, 1):
                    if i != int(num.split('=')[0].strip()):
                        print('config錯誤')
                        return 0
                    else:
                        tmp_list.append(num.split('=')[1].strip())
                if not len(tmp_list):
                    tmp_list = None
                All_Same_Chapter[chapter]['inner_title_and_file_name'] = deepcopy(tmp_list)
    

    print(All_Same_Chapter)

    return data


    
    


if "__main__" == __name__:
    load_ini(config_path)
   

