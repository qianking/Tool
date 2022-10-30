import time 
import threading
from threading import Thread, get_ident
from collections import defaultdict
import time


class CustomLocal(object):
    def __init__(self):
        #self.storage = {}
        super(CustomLocal, self).__setattr__("storage", {})

    def __setattr__(self, key, value):
        ident = get_ident()
        if ident in self.storage:
            self.storage[ident][key] = value
        else:
            self.storage[ident] = {key: value}
    
    def __getattr__(self, item):
        ident = get_ident()
        return self.storage[ident][item]

local = CustomLocal()


tls = defaultdict(dict)


def get_thread_ctx():
    """ Get thread-local, global context"""
    return tls[threading.get_ident()]



""" 
class SingleTonNew():  

    _instance = None
    a = 5

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance
    
    def clear_all(self):
        self.a = 5 """

class SingleTonNew(object):
    _instance = None
    a = 5
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
        
    

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Borg:
    __monostate = None
    a = 5
    t= 4

    def __init__(self):
        if not Borg.__monostate:
            Borg.__monostate = self.__dict__
            #Your definitions here
            self.x = 1

        else:
            self.__dict__ = Borg.__monostate

