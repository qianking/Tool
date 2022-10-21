from concurrent.futures import ThreadPoolExecutor
import test_1


class nn():
    oo = None

    def __init__(self, pp):
        self.oo = pp
        self.tt = test_1.tt(self.oo)
        self.tt.ttt()

    

def uu():
    i = [1, 2 ,3]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            oooo = nn(p)
            futures = executor.submit(oooo)

uu()