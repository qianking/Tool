
class ppp():
    a = 5

class SingleTonNew:  
    def __new__(cls, *args, **kwargs): 
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.i = ppp()

