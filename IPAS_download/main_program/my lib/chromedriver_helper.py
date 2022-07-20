import os 
import zipfile
import requests
from requests_ntlm import HttpNtlmAuth
import sys
sys.path.append(r"C:\littleTooldata\IPLAS\program\my lib")
import file_util
from userlogin_UI import return_user_data
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_lastestdriverversion_url = "http://chromedriver.storage.googleapis.com"
chrome_driver_folder = r"C:\littleTooldata\seleniumdriver\chrome"
chrome_driver_mapping_file = r"{}\mapping.json".format(chrome_driver_folder)
chrome_driver_exe = r"{}\chromedriver.exe".format(chrome_driver_folder)
chrome_driver_zip = r"{}\chromedriver_win32.zip".format(chrome_driver_folder)
chrome_driver_log = "C://littleTooldata//seleniumdriver//logs"

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
    #print(password[0], password[1])
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

''' def download_chromedriver():
    
    chrome_major_ver = get_chrome_driver_verion()
    lastest_driver_ver = last_driver_ver(chrome_major_ver)
    download_driver(lastest_driver_ver, chrome_driver_folder)
    unzip_driver_to_target_path(chrome_driver_zip, chrome_driver_folder)
    data = { 
            chrome_major_ver : {
                "driver_path" : chrome_driver_exe,
                "driver_version": lastest_driver_ver,
            }
        }
    file_util.write_json(chrome_driver_mapping_file, data)
    Chromedriver_logger.info("driver version update success")

def check_chromedriver():
    
    if not os.path.exists(chrome_driver_exe):
        create_driver_file(chrome_driver_folder)
        Chromedriver_logger.info("not find chrome driver")
        download_chromedriver()
        
    else:
        try:
            s = Service(chrome_driver_exe)
            options = Options()
            options.add_argument("--disable-gpu")
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option("detach", True)
            options.add_experimental_option('excludeSwitches', ['enable-logging'])  
            options.add_argument("--headless")
            driver = webdriver.Chrome(service = s, options = options)
            driver.minimize_window()
            driver.get('https://www.google.com.tw/')
            time.sleep(1)
            driver.quit()
            print("fine")
            
        except Exception:
            Chromedriver_logger.info("detect old driver version")
            download_chromedriver()
        
        else:
            Chromedriver_logger.info("chrome driver already") '''
            

def check_driver_available():
    last_driver_version = 0
    last_check_time = None
    create_driver_file(chrome_driver_folder)
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
    