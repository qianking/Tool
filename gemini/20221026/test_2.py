from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew
from test_4 import jj




def uu():

    n= SingleTonNew()
    n.t = 'hello'
    print('n.a:', n.a)
    i = [1, 2, 9]
    #Main(i[0])
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            futures = executor.submit(Main(p)) 



class llll():

    uuu = SingleTonNew()

    def __init__(self):
        pass

    def test_6(self, b):
    
        self.uuu.a += b
        print(self.uuu.a)


class pppp(jj, llll):

    ooo = SingleTonNew()

    def __init__(self):
        super().__init__()

    def test(self, b):
        self.test_6(b)

        self.add(b)
        print(self.ooo.a)

    

def Main(b):
    sin = SingleTonNew()
    run_time = 1
    print(sin.t)
    while run_time != 4:
        
        oo = pppp()
        oo.test(b)
        print(sin.a)
        print(sin.p)
        run_time += 1
        sin.clear_all()

def ii():
    n= SingleTonNew()
    print(n.p)
    n.clear_all()
    n.tess('world')

def ooooo():
    n= SingleTonNew()
    n.tess('hello')
    ii()
    print(n.p)

#ooooo()

uu()

