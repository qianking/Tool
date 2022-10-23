from test_3 import SingleTonNew
from functools import wraps



class Fail_Dealer():
    def __init__(self):
        self.jjj = SingleTonNew()

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            func(*args, **kwargs)
            print('no')
            print(self.jjj.i.a)

        return decorated

class jj():
    
    pp = SingleTonNew()

    def __init__(self):
        pass
    
    @Fail_Dealer()
    def add(self, b):
        self.pp.i.a += b
        print(self.pp.i.a)