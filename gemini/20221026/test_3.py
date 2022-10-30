
class ppp():
    t= ''
    a = 5

class SingleTonNew(ppp):  

    _instance = None
    p = ''

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 
    
    
    def tess(self, pp):
        self.p += pp
        
    def clear_all(self):
        self.a = 5

