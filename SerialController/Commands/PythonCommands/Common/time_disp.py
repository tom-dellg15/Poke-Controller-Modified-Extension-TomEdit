import datetime

class Test_time_disp():
    NAME = '【共通】時刻表示'

    def __init__(self):
        super().__init__()

    def do(self):
        print(datetime.datetime.now())
