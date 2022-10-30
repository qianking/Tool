from concurrent.futures import ThreadPoolExecutor
from test_3 import SingleTonNew, Borg, get_thread_ctx, CustomLocal
from threading import Thread, get_ident
from test_4 import ADD_2
import threading
import time



def Main_Thread():
    i = [1, 2 , 9]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for p in i:
            futures = executor.submit(Main, p) 
            time.sleep(0.1)

    
def Main(b):
    tmp = SingleTonNew()
    print(id(tmp))
    ident = get_ident()
    #print(ident)
    tmp.a = 5
    print('tmp.a:', tmp.a)
    

    l = ADD_2(b)  
    l.add()
       

Main_Thread()

