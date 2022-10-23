from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew
from test_4 import jj




def uu():
    i = [1, 2, 9]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            futures = executor.submit(Main(p))

class pppp():

    ooo = SingleTonNew()

    def __init__(self):
        self.j = jj()

    def test(self, b):

        self.j.add(b)
        print(self.ooo.i.a)

    

def Main(b):
    sin = SingleTonNew()
    oo = pppp()
    oo.test(b)
    print(sin.i.a)


uu()

