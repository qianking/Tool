from test_3 import SingleTonNew
from functools import wraps
import sys
import traceback

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

class jj(metaclass = myMetaClass):
    
    pp = SingleTonNew()

    def __init__(self):
        pass

    def add(self):
       print('nn')
       print('in add:', sys._getframe(1).f_code.co_name)


def get_function_name():
    return sys._getframe(1).f_code.co_name
    
class hh():
    ff = jj()

    def test(self):
        self.ff.add()



oo = hh()
oo.test()