from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew
from test_4 import jj




def uu():
    i = [1, 2, 9]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            futures = executor.submit(Main(p))

def Main(b):
    sin = SingleTonNew()
    oo = jj(b)
    print(sin.i.a)
uu()
