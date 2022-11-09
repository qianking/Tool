import binascii
from pyDes import des, CBC, PAD_PKCS5

key = '98041652'

def Encrypt(s):
    k = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

def Decrypt(s):
    k = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    de = de.decode()
    return de



    





