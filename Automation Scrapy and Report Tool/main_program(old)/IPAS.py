import argparse
import sys
import os


'''
先檢查網路以及使用者帳密，然後傳入Download_isn.py
'''
'''
再檢查chrome_driver，得到chromedriver的位址

'''

'''
如果有外部參數傳進來則為每日執行下載的動作，那就執行Download_isn.py那個檔案, 傳入參數、使用者資料和chromedriver的位址
'''

'''
如果沒有外部參數傳進來，則為重UI傳進來, 傳入參數、使用者資料和chromedriver的位址
'''


args = parser.parse_args()
if args.all != None:
    All_project = args.all
    User_select_project = args.pro[0]
    Time_selection = args.time[0].replace('_', " ")
    Time_selection_index = int(args.time[1])
    Time_period = args.time[2]
    Time_period = Time_period.replace('_',' ')
    Time_period = Time_period.replace('+','~')

    Check_box_default_temp = args.check
    for i in Check_box_default_temp:
        Check_box_default.append(int(i))
    File_download_path = args.path[0]



def get_args_from_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-all', type = str, nargs='+')
    parser.add_argument('-pro', type = str, nargs='+')
    parser.add_argument('-time', type = str, nargs='+')
    parser.add_argument('-check', type = str, nargs='+')
    parser.add_argument('-path', type = str, nargs = 1)
    return parser