from SFIS import SFIS
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor
import datetime
import re
import inspect
import traceback
import read_ini




def print_time(func):
    def warp():
        print("Now the Unix time is {}".format(int(time.time())))
        func()
        print(func.gggg)
    return warp

@print_time
def test():
    gggg = 'pppp'

test()