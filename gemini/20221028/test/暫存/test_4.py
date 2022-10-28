from test_3 import SingleTonNew
from functools import wraps
import sys
import traceback



class Fail_Dealer():
    def __init__(self):
        self.jjj = SingleTonNew()

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):

            func(*args, **kwargs)
            print('in decorator:', traceback.extract_stack(None, 2)[0][2])

            print(self.jjj.a)

        return decorated

class jj():
    
    pp = SingleTonNew()

    def __init__(self):
        pass
    
    @Fail_Dealer()
    def add(self):
       print('nn')
       print('in add:', traceback.extract_stack(None, 2)[0][2])


def get_function_name():
    return traceback.extract_stack(None, 2)[0][2]
    
class hh():
    ff = jj()

    def test(self):
        self.ff.add()



oo = hh()
oo.test()