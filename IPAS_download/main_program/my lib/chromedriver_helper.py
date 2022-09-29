import os 
import zipfile
import requests
from requests_ntlm import HttpNtlmAuth
import file_util
from User_login import return_user_data
import datetime

chrome_lastestdriverversion_url = "http://chromedriver.storage.googleapis.com"

current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])

chrome_driver_folder = os.path.join(upper_folder_path, "data")
chrome_driver_mapping_file = os.path.join(chrome_driver_folder, "mapping.json")
chrome_driver_exe = os.path.join(chrome_driver_folder, "chromedriver.exe")
chrome_driver_zip = os.path.join(chrome_driver_folder, "chromedriver_win32.zip")
chrome_driver_log_folder = os.path.join(upper_folder_path, "logs")
chrome_driver_log = os.path.join(chrome_driver_log_folder, "chromedriver")


#在pega內部使用request設定
password = return_user_data()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
proxies = {"http":"proxy8.intra:80"}
auth = HttpNtlmAuth(password[0], password[1])

Chromedriver_logger = file_util.create_logger(chrome_driver_log, 'Chromediver_log')

def date_transfer(date):
    if date is not None:
        day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return day
        
def get_now_time():
    now = datetime.datetime.now()
    now = str(now)
    now = now.split('.')[0]
    return now


def create_driver_file(driver_folder):
    if not os.path.isdir(driver_folder):
        os.makedirs(driver_folder)
        Chromedriver_logger.info(f"create file: '{driver_folder}'")
        

def get_chrome_driver_verion():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_version = file_util.get_file_version(chrome_path)
    chrome_major_ver = chrome_version.split(".")[0]
    return chrome_major_ver


def last_driver_ver(chrome_major_ver):
    url = chrome_lastestdriverversion_url + f"/LATEST_RELEASE_{chrome_major_ver}"
    
    try:
        resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300)
        print(resp.status_code)
    except Exception as Argument: 
        Chromedriver_logger.exception(f"connect '{url}' failed")
    else:
        lastest_driver_ver = resp.text.strip()
        return lastest_driver_ver
    


def download_driver(lastest_driver_version, des_folder):
    download_api = f"{chrome_lastestdriverversion_url}/{lastest_driver_version}/chromedriver_win32.zip"
    dest_path = os.path.join(des_folder, os.path.basename(download_api))
    resp = requests.get(url = download_api,headers = headers, proxies=proxies, auth = auth, timeout=300)
    print(resp.status_code)
    if resp.status_code == 200:
        with open (dest_path, 'wb') as f:
            f.write(resp.content)
        Chromedriver_logger.info("driver download successful")
    else:
        Chromedriver_logger.error("driver download failed")


def read_driver_mapping():
    driver_mapping = {}
    if os.path.exists(chrome_driver_mapping_file):
        driver_mapping = file_util.read_json(chrome_driver_mapping_file)
        
    return driver_mapping


def unzip_driver_to_target_path(from_path,des_path):
    with zipfile.ZipFile (from_path, 'r') as zip:
        zip.extractall(des_path)
    Chromedriver_logger.info("unzip [{}] -> [{}]".format(from_path, des_path)) 


def check_driver_available():
    last_driver_version = 0
    last_check_time = None
    create_driver_file(chrome_driver_folder)
    create_driver_file(chrome_driver_log)
    driver_mapping = read_driver_mapping()
    now = get_now_time()
    nowday = date_transfer(now)
    for key, value in driver_mapping.items():
        last_check_time = value['last_check_time']
        Chromedriver_logger.info(f"==============================================================")
        Chromedriver_logger.info(f'get last check time: {last_check_time}')
    last_check_day = date_transfer(last_check_time)

    if (last_check_day is None) or ((nowday-last_check_day).days >= 10):
        Chromedriver_logger.info("check driver version")
        chrome_major_ver = get_chrome_driver_verion()
        lastest_driver_ver = last_driver_ver (chrome_major_ver)
        last_check_time = now  
        for key, value in driver_mapping.items():
            last_driver_version = value['driver_version']
        if last_driver_version != lastest_driver_ver:
            download_driver(lastest_driver_ver, chrome_driver_folder)
            unzip_driver_to_target_path(chrome_driver_zip, chrome_driver_folder)
            data = { 
                chrome_major_ver : {
                    "driver_path" : chrome_driver_exe,
                    "driver_version": lastest_driver_ver,
                    "last_check_time": last_check_time
                }
            }
            file_util.write_json(chrome_driver_mapping_file, data)
            Chromedriver_logger.info("driver version update")
        else: 
            data = { 
                chrome_major_ver : {
                    "driver_path" : chrome_driver_exe,
                    "driver_version": lastest_driver_ver,
                    "last_check_time": last_check_time
                }
            }
            file_util.write_json(chrome_driver_mapping_file, data)
            Chromedriver_logger.info("no newest version")


def return_driver_path():
    return chrome_driver_exe 
    

if __name__ == "__main__":
    
    check_driver_available()
    