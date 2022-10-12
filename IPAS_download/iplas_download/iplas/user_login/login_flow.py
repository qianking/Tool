import sys
import os
import requests
from requests_ntlm import HttpNtlmAuth
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))))
sys.path.append("./lib")
import _crypt
import urllib3

urllib3.disable_warnings()

def check_user_data(user_data_path, userdata, signal):
    code = _checkpass_request(userdata)
    
    if code == 200:
        data = ' '.join(userdata)
        en_data = _crypt.Encrypt(data)
        with open(user_data_path, 'wb') as f:
            f.write(en_data)
    signal.result.emit(code)    

def _checkpass_request(data):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    proxies = {"http":"proxy8.intra:80"}
    auth = HttpNtlmAuth(data[0], data[1])
    url = 'http://eip.tw.pegatroncorp.com/'
    try:
        resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300, verify=False)

    except Exception as ex:
        print('登入驗證錯誤 error : ', ex)
        return 404 

    else:
        return resp.status_code

def _test(userdata):
    data = ' '.join(userdata)
    en_data = _crypt.Encrypt(data)
    with open(user_data_path, 'wb') as f:
        f.write(en_data)

if __name__ == "__main__":
    user_data_path = r'D:\Qian\python\GIT\Tool\IPAS_download\iplas_download\docs\fw7ssv7b9bdb7ddn'
    data = ['Andy_Chien', 'pega#6543216']
    #_test(data)
    print(_checkpass_request(data))