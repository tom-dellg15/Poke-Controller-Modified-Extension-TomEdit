import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE2_util import EXE2_util

class EXE2LocalTradeNoChip(EXE2_util):
    NAME = '【EXE2】リセット'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用リセット処理_v1.0 Release.2024/10/16
     Copyright(c) 2024 tom dp
     ◆改修内容
        ・
        ・
    --------------------------------------------------------------------------------------
    '''
    # initの中に実行コマンドはかけないっぽい
    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui

        self.debug_flag = True

    def do(self):
        self.EXExPrint(
            "▼▼▼リセット開始▼▼▼"
        )
        # 時刻表示
        self.EXExPrint(
            str(datetime.datetime.now())
        )
        
        # オプション画面 -> タイトル画面へ
        time1 = 0.3
        time2 = 0.5
        time3 = 1.4
        time4 = 2.0 #1.9~
        self.press(Button.MINUS, wait=time2)
        self.press(Hat.TOP, wait=time1)
        self.press(Hat.TOP, wait=time1)
        self.press(Button.A, wait=time1)
        self.press(Hat.LEFT, wait=time1)
        self.press(Button.A, wait=time1)
        templatePass = self.EXExGetTemplPass("_title.png")
        # タイトル画面が出るまで待機
        while not self.isContainTemplate(templatePass, threshold=0.9):
            # 何もしない
            pass
        self.press(Button.PLUS, wait=time1)
        self.press(Button.PLUS, wait=time3)
        # ミステリーデータ入手
        self.press(Button.A, wait=time4)
        self.press(Button.A, wait=time1)

        self.EXExPrint(
            "▲▲▲リセット終了▲▲▲"
        )

