from concurrent.futures import thread
import threading
class ppp():
    t= ''
    a = 5

class variable():
    total = {}

    def __init__(self):
        ident = threading.get_ident()
        if ident not in self.total:
            self.total[ident] = {}
 
    def __getattr__(self, item):
        ident = threading.get_ident()
        return self.total[ident][item]
    def __setattr__(self, a = None, b = None):
        ident = threading.get_ident()
        self.total[ident] = {a:b}
        return 
        

''' class SingleTonNew(ppp):  

    _instance = None
    p = ''

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance  '''
    
    




class SingleTonNew(dict):  

    def __new__(cls):
        ident = threading.get_ident()
        if not hasattr(cls, 'instance'):
            cls._variable = super(SingleTonNew, cls).__new__(cls)
            if  ident not in cls._variable:
                cls._variable[ident] = super(SingleTonNew, cls).__new__(cls, ident)

        return cls._variable[ident]
    
    def create_variable(self):
        ident = threading.get_ident()
        self._variable[ident]['b'] = lambda data: fff(data)
    



def fff(data:dict):
    for i, g in data.items():
        g += 10
        return g
    
