from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew, variable
from test_4 import jj
import threading
import time



def uu():

    n= SingleTonNew()
    print("n:", threading.get_ident())
    n.create_variable()
    print(n['b']({'g':5}))
    i = [1, 5, 10]
    #Main(i[0])
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            futures = executor.submit(Main, p) 
            time.sleep(0.1)
    
    print(n)





class llll():


    def __init__(self, v):
        

    
    

def Main(p):
    sin = SingleTonNew()
    print('id sin:', id(sin))
    sin.create_variable()
    print("Main:", threading.get_ident())
    run_time = 1
    if p == 1:
        sin['a'] =p
    print(sin.get('a'))
    sin['b'] = {'g':5}
    print(sin['b'])
    iii = jj()
        
    


uu()
    

