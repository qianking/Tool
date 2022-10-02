import sys
import os
#import threading
import time
import threading
import ctypes
import time
#from threading import Thread



class test_flow(threading.Thread):
    def __init__(self):
        super(test_flow, self).__init__() 
        self.fff= None 

    def test(self, ooo = None):
        try:
            for i in range(100000):
                
                print(i)
                time.sleep(1)
        finally:
            print('ended')
    
    def stop(self, ooo):
        if ooo:
            raise Exception('stop')






    


