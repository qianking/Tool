class TimeOutError(Exception):
    pass

class TestItemFail(Exception):
    """
    填入 
    測項名稱, 如果跟測試項目名稱一樣就填None
    測項參數(值, 下限, 上限)(如果沒有就填None), 
    """
    def __init__(self, test_item = None, data = None, error = None):
        if not data:
            super().__init__((test_item, (None, None, None), error))
        else:
            super().__init__((test_item, data, error))

class Test_Fail(Exception):
    pass


class Online_Fail(Exception):
    pass

       
        


