from copy import deepcopy
from functools import partial
from enum import Enum
from test_3 import SingleTonNew
from datetime import datetime
import traceback
import inspect
import sys
     
         


''' class func():
    def funcA(data):
        return data+1

    def funcB():
        print('B')

    def funcC():
        print('C')


class Model_seletion(Enum):
    model_A = partial(func.funcA)
    model_B = partial(func.funcB)
    model_C = partial(func.funcC)

    def __call__(self, *args, **kwargs):
        oo = self.value(*args, **kwargs)
        return oo

o = Model_seletion.model_A
print(o(5)) '''
''' a = 1  
while a != 10:
    print('o')
    a+=1
print(a) '''

def track_func():
    
    return 
def iiiii():
    oo = sys._getframe(1).f_code.co_name

    print(oo)
    print('ggg')


def jjj():
    iiiii()



jjj()

