from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew, variable
from test_4 import jj
import threading
import time



def uu():

    k= SingleTonNew()
    n = k[threading.get_ident()]

    n['t'] = 'hello'
    print('n.a:', n['t'])
    i = [1]
    #Main(i[0])
    with ThreadPoolExecutor(max_workers=len(i)) as executor:
        for p in i:
            futures = executor.submit(Main, p) 
            time.sleep(0.1)
    
    print('exception:', futures.exception())





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
    s= SingleTonNew()

    sin = s[threading.get_ident()]

    #sin.create_variable()
    print("Main:", threading.get_ident())
    sin['a'] = p
    print('in main:', sin['a'])
   
    iii = jj()
    iii.add()
    print(sin['a'])
    print(s)
    

        
    
    


#ooooo()

uu()
    

