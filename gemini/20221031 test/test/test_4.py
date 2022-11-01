<<<<<<< Updated upstream:gemini/20221029/test_4.py
from test_3 import SingleTonNew, variable
import threading
from functools import wraps
import sys
import traceback
import time
=======
from test_3 import SingleTonNew, Borg, get_thread_ctx, CustomLocal
from functools import wraps
import sys
import traceback
from test_1 import ADD_1



class ADD_2():
    
    pp = SingleTonNew()

    def __init__(self, b):
        #print(self.pp['a'])
        self.b = b
        self.ggg = ADD_1(b)
        self.ggg.add()

    def add(self):
        self.pp.a += self.b
        print("in ADD_2 a before:", self.pp.a)
    




>>>>>>> Stashed changes:gemini/test/test_4.py

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if not len(bases) and callable(value) and attr != '__init__':
                local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local)

class Fail_Dealer():
    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                func(*args, **kwargs)
                print('in decorator:', sys._getframe(1).f_code.co_name)
            except Exception:
                print('exception')


        return decorated

<<<<<<< Updated upstream:gemini/20221029/test_4.py
        

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



       
=======




class MAIN():

    @staticmethod
    def test_1():
        print('in test_1')
        

    def test_2(self):
        raise Exception
        print('in test_2')
        
>>>>>>> Stashed changes:gemini/test/test_4.py

    @Fail_Dealer()
    def main(self):
        self.test_1()
        self.test_2()


    

def get_function_name():
    return sys._getframe(1).f_code.co_name

a= [0, 2003, 2004, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
i = 0

<<<<<<< Updated upstream:gemini/20221029/test_4.py
def ooo():
    for o in a:
        return i+1 if o else i
print(ooo)   
=======
>>>>>>> Stashed changes:gemini/test/test_4.py
