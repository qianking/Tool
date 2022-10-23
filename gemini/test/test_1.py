from copy import deepcopy
from functools import partial
from enum import Enum
from test_3 import SingleTonNew

a = 5       
         


class func():
    def funcA(data):
        print(data)

    def funcB():
        print('B')

    def funcC():
        print('C')


class Model_seletion(Enum):
    model_A = partial(func.funcA)
    model_B = partial(func.funcB)
    model_C = partial(func.funcC)

    def __call__(self, *args, **kwargs):
        self.value(*args, **kwargs)








