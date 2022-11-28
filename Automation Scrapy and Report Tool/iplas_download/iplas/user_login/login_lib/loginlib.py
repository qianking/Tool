import binascii
from pyDes import des, CBC, PAD_PKCS5
import urllib3
import requests
from requests_ntlm import HttpNtlmAuth


key = '98041652'


urllib3.disable_warnings()

def Encrypt(s):
    k = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

def Decrypt(s):
    k = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    de = de.decode()
    return de


def checkpass_request(data):
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



    





