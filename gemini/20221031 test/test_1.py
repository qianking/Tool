from copy import deepcopy
from functools import partial
from enum import Enum
from test_3 import SingleTonNew
from test_3 import SingleTonNew, Borg, get_thread_ctx, CustomLocal
from datetime import datetime
import traceback
import inspect
import sys
import time
<<<<<<< Updated upstream:gemini/20221029/test_1.py
     
         
now_day = datetime.now().strftime("%m/%d")
print(now_day)
=======
from test_3 import SingleTonNew

>>>>>>> Stashed changes:gemini/test/test_1.py

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

class ADD_1():
    
<<<<<<< Updated upstream:gemini/20221029/test_1.py
    print('yy')
    iii()
    return 'p', 5

i = 'jjjjj'

sfis_seperate = f"{ 'SFIS':-^50}\r\n"
print(sfis_seperate)

=======
    pp = SingleTonNew()

    def __init__(self, b):
        self.b = b
        
    def add(self):
        self.pp.a += self.b
        print("in ADD_1 a:", self.pp.a)
>>>>>>> Stashed changes:gemini/test/test_1.py
