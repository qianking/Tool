from copy import deepcopy
from functools import partial
from enum import Enum
from test_3 import SingleTonNew
from datetime import datetime
import traceback
import inspect
import sys
import time
import shutil

def kkkk():
    print(iiii())

def iiii():
    
    return traceback.extract_stack(None, 2)[0][2]




def deal_hw_test_name(test_name:str):
    test_name = test_name.replace('-', ' ')
    test_name = [i for i in test_name.split(' ') if i.strip()!='']
    test_name = '_'.join(test_name)
    test_name = test_name.lower()
    return test_name

''' print(deal_hw_test_name('CPLD  (CPU) - FW ver'))

o = "MAC: Marvell Technology Group Ltd. Device 8400 , LnkSta: Speed 8GT/s , Width x2"
print(o.split(':', 1)) '''

def is_num(num):
    try:
        int(num)
    except:
        pass

    else:
        return int(num)
    
    try:
        float(num)
    
    except:
        pass

    else:
        return float(num)




def pppp(command, *fff):
    print(command)
    print(fff)


a = ['A', 'B', 'B', 'E', 'D', 'C']
b = ['A', 'C', 'B', 'E', 'E', 'C']

print( len([1 for a, b in zip(a, b) if a != b]) )