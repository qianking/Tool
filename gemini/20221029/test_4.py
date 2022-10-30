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
    def __init__(self):
        self.jjj = SingleTonNew()

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):

            func(*args, **kwargs)
            print('in decorator:', sys._getframe(1).f_code.co_name)

            print(self.jjj.a)

        return decorated

        

class jj():

    v = SingleTonNew()

    def __init__(self): 
        self.j = self.v._variable[threading.get_ident()]
        print('id v:', id(self.v))
        print('in jj:', threading.get_ident()) 
        print(self.v._variable)
        print(self.j.get('a'))
        i = 0
        while i!= 50:
            i+=1
            time.sleep(0.5)



       


def get_function_name():
    return sys._getframe(1).f_code.co_name

a= [0, 2003, 2004, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
i = 0

def ooo():
    for o in a:
        return i+1 if o else i
print(ooo)   