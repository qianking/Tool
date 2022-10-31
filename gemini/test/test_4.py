from test_3 import SingleTonNew, variable
import threading
from functools import wraps
import sys
import traceback
import time

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if not len(bases) and callable(value) and attr != '__init__':
                local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local)

class Fail_Dealer():

    oo = SingleTonNew()

    def __init__(self):
        self.o = self.oo[threading.get_ident()]
        print(self.o)
        

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            
            func(*args, **kwargs)
            print(self.o)
            
        return decorated

class jj(metaclass = myMetaClass):

    l = SingleTonNew()

    def __init__(self): 
        ident = threading.get_ident()
        self.v = self.l[ident] 
        print('in jj:', id(self.v))

    def add(self):
        print(threading.get_ident())
        i = 0
        while i!=10:
            i+=1
            time.sleep(0.5)

        self.v['a'] += 1
       

       
def get_function_name():
    return sys._getframe(1).f_code.co_name

