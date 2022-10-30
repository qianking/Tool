import re
import sys

test = 'System serial number            : PSZ23231D2S'
test_2 = 'Console(pega)#'
test_3 = ''

class Find_Method():
    
    @staticmethod
    def FindString(data_strings, findstring, *splitstr): 
        """
        尋找特定字串否有在裡面
        如果splitstr有參數(分割的符號)，那就是尋找分割符號後面的字串
        (資料、要找的字串、*分隔符號)
        """   
        if len(splitstr) == 0:
            if findstring in data_strings:
                return True
            else:
                return False
            
        else:
            splitstr = splitstr[0]
            pattern = rf'{findstring}\s*{splitstr}(\s*.*\s*)'
            txt = re.findall(pattern, data_strings)
            if len(txt) != 0:
                txt = txt[0].strip()
                return txt

    @staticmethod
    def FindValueinForm(data_strings, col_startword, splitstr, goal_col_num):
        """
        尋找表單中要找的目標(資料、尋找的欄開頭文字、表單分隔符號、目標欄數)
        """
        pattern = rf'{col_startword}.*[\r\n]'
        txt = re.findall(pattern, data_strings)
        txt = txt[0].split(splitstr)
        tmp_list = [i for i in txt if i != '']
        goal_value = tmp_list[goal_col_num-1]
        return goal_value


class Extract_Method():
    """
    使用正則表達式來提取資料
    """
    @staticmethod
    def Extract_Data(search_word, search_data):
        """
        非貪婪搜尋，有使用re.DOTALL方法
        """
        pattern = re.compile(search_word, re.DOTALL)
        data = pattern.findall(search_data)[0]
        return data

    def Get_Number(search_data):
        pattern = re.compile(r'(\d+[.]*\d*)', re.DOTALL)
        data = pattern.findall(search_data)[0]
        try:
            data = int(data)
        except:
            data = float(data)
        return data


if "__main__" == __name__:
    print(Extract_Method.Get_Number(' +56.0 C (high = +82.0 C, crit = +104.0 C)'))
    #print(FindValueinForm(test_3, '0/16', ' ', 3))
    #abc()
       

