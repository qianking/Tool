from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew, variable
from test_4 import jj
import threading
import time



def uu():

    n= SingleTonNew()
    print("n:", threading.get_ident())

    n['t'] = 'hello'
    print('n.a:', n['t'])
    i = [1]
    #Main(i[0])
    with ThreadPoolExecutor(max_workers=1) as executor:
        for p in i:
            futures = executor.submit(Main, p) 
            time.sleep(0.1)





class llll():


    def __init__(self, v):
        pass

    def test_6(self, b):
    
        self.uuu.a += b
        print(self.uuu.a)


''' class pppp(jj):

    v= SingleTonNew()

    def __init__(self):
        self.v.a = 5
    def test(self):
        self.add()
        print(self.v.a)
         '''
    

def Main(p):
    sin = SingleTonNew()
    print("Main:", threading.get_ident())
    run_time = 1
    sin['a'] =p
    print(sin['a'])
    iii = jj()
    iii.add()

        
    
    

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
    

