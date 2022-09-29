from asyncio import tasks
from multiprocessing.pool import ThreadPool
import os
import time
import sys
import binascii
from pyDes import des, CBC, PAD_PKCS5
from glob import glob
import getpass
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent.futures import as_completed
''' current = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current, 'test')
print(current)
last_folder_path = '\\'.join(current.split('\\')[:-1])
print(last_folder_path) '''


''' def Encrypt(key, s):
    iv = key
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

def Decrypt(key, s):
    iv = key
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de



secret_str = Encrypt('12345678', 'Qianking0706+')
print(secret_str)
with open(path, 'wb') as f:
    f.write(secret_str)

with open(path, 'rb') as f:
    secret = f.readline()
clear_str = Decrypt('12345678', secret)
clear_str = clear_str.decode()
print(clear_str) '''


''' threadLocal = threading.local()

chrome_driver_path = r'C:\littleTooldata\seleniumdriver\chrome\chromedriver.exe'
def getdriver():
    servic = Service(chrome_driver_path)
    options = Options()
   
    #options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("detach", True)   
    options.add_experimental_option('excludeSwitches', ['enable-logging'])        
    driver =  webdriver.Chrome(service = servic, options = options)
    return driver
#driver_a = getdriver()
driver_log = []

def get_driver():
    global driver_log
    driver =  getattr(threadLocal, 'driver', None)
    if driver is None:
        driver = getdriver()
        driver_log.append(driver)
        setattr(threadLocal, 'driver', driver)
        print(threadLocal)
    else:
        print(threadLocal)
    return driver

def test(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(5)
    get_url = driver.current_url
    print(f"The current url is {get_url}")
    return get_url '''

''' def test_2(url):
    driver_a.get(url)
    time.sleep(5)
    get_url = driver_a.current_url
    print(f"The current url is {get_url}")
    return get_url '''

''' def main():
    start_time = time.time()
    url_list = [r'https://translate.google.com.tw/?hl=zh-TW&tab=rT',
    r'https://www.google.com.tw/?hl=zh_TW',
    r'http://eip.tw.pegatroncorp.com/',
    r'https://docs.python.org/2/library/queue.html',
    r'https://leetcode.com/problems/letter-combinations-of-a-phone-number/']
    #ThreadPool(3).map(test, url_list)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = executor.map(test, url_list)
    
    print('*'*20)
    for future in futures:
        print(future)
    print('driver_log', driver_log)
    #map(lambda d:d.close(), driver_log)
    for x in driver_log:
        x.close()
        x.quit() 
    end_time = time.time()
    print(f'cost time {end_time-start_time}')

def main_2():
    a = [1,2,3,4,5,6]
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = executor.map(test_2, a)
    print('*'*20)
    for future in futures:
        print(future)

def test_2(n):
    print(n)
    time.sleep(2)
    return n**2

def main_3():
    start_time = time.time()
    threads = []
    url_list = [r'https://translate.google.com.tw/?hl=zh-TW&tab=rT',
    r'https://www.google.com.tw/?hl=zh_TW',
    r'http://eip.tw.pegatroncorp.com/',]
    for u in url_list:
        th = threading.Thread(target=test, args=(u,))  
        th.start()
        threads.append(th)
    end_time = time.time()
    print(f'cost time {end_time-start_time}') '''
    
    
    

''' def main_t():
    start_time = time.time()
    url_list = [r'https://translate.google.com.tw/?hl=zh-TW&tab=rT',]
    for i in url_list:
        test_2(i)
    driver_a.close()
    driver_a.quit()
    end_time = time.time()
    print(f'cost time {end_time-start_time}') '''

''' a = ['a', 'b', 'c', 'd', 'e', 'f']
for i in a[:]:
    if i =='b':
        a.remove('b')
print(a)
 '''
''' def print_p(txt):
    time.sleep(10)
    print(f'in print_p, print txt: {txt}')

def test_sleep(t):
    print(f"thread start {threading.current_thread().name}")
    time.sleep(t)
    print(f"thread end {threading.current_thread().name}")
    return t
with ThreadPoolExecutor(max_workers=10) as executor:
    y = [2, 2, 2, 2, 5]
    datas = [executor.submit(test_sleep, t) for t in y]
    while executor._work_queue.qsize() > 0:
        for d in as_completed(datas, timeout=11):
            if d.result() == 2:
                f = executor.submit(print_p, d.result())
    
            
    print('done') '''



if 5 in range(3, 6):
    print(99999999)


