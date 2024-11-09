#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import PythonCommand
from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim


# Get watt automatically using the glitch
class InfinityWatt(ImageProcPythonCommandTrim,PythonCommand):
    NAME = '【剣盾】無限ワット'

    def __init__(self, cam, gui=None):
        super().__init__(cam)
        self.cam = cam
        self.gui = gui
        self.use_rank = False
        self.i = 0

    def do(self):
        # Bを0.5秒間隔で5回押す
        self.pressRep(Button.B, repeat=5, interval=0.5)
        while True:
            self.wait(1)

            if self.use_rank:
                #self.timeLeap()
                self.timeLeapMod()

                self.press(Button.A, wait=1)
                self.press(Button.A, wait=1)  # 2000W
                self.press(Button.A, wait=1.8)
                self.press(Button.B, wait=1.5)

            else:
                self.press(Button.A, wait=1)
                # ワット取得
                if self.isContainTemplate('InfinityUtil\watt_msg_Eng.png',threshold=0.9): 
                    self.press(Button.A, wait=1)
                # 2000W
                if self.isContainTemplate('InfinityUtil\watt_Eng.png',threshold=0.9): 
                    self.press(Button.A, wait=1)
                    self.press(Button.A, wait=1)
                    self.i += 1
                    print("取得ワット数：" + str(self.i * 2000) + " 時刻：" + str(datetime.datetime.now()))
                # レイド開始
                self.press(Button.A, wait=2)
                # タイムリーディング
                #while not self.isContainTemplate('InfinityUtil\time_Eng.png'): 
                #    self.wait(0.5)
                self.wait(3)

                self.press(Button.HOME, wait=1)
                self.press(Direction.DOWN)
                self.press(Direction.RIGHT)
                self.press(Direction.RIGHT)
                self.press(Direction.RIGHT)
                self.press(Direction.RIGHT)
                self.press(Direction.RIGHT) #追加
                self.press(Button.A, wait=1.5)  # 設定選択
                self.press(Direction.DOWN, duration=2, wait=0.5)

                self.press(Button.A, wait=0.3)  # 設定 > 本体
                count = 0
                while not self.isContainTemplate('InfinityUtil\setting_main_body_datetime_Eng.png',threshold=0.9): 
                    self.press(Direction.DOWN, wait=0.3)    #追加
                    count += 1
                    if count > 60:
                        print("設定＞日付と時刻 選択エラー")
                        break
                    #self.press(Direction.DOWN)
                    #self.press(Direction.DOWN)
                    #self.press(Direction.DOWN)
                    #self.press(Direction.DOWN, wait=0.3)
                    #self.press(Direction.DOWN, wait=0.3)    #追加
                    #self.press(Direction.DOWN, wait=0.3)    #追加
                    #self.press(Direction.DOWN, wait=0.3)    #追加
                    #self.press(Direction.DOWN, wait=0.3)    #追加
                    #self.press(Direction.DOWN, wait=0.3)    #追加（予備）　日付と時刻にカーソルが当たるまで下に行く処理に変える
                self.press(Button.A, wait=0.2)  # 日付と時刻 選択
                # コメント化
                # self.press(Button.A, wait=0.4)

                self.press(Direction.DOWN, wait=0.2)
                self.press(Direction.DOWN, wait=0.2)
                self.press(Direction.DOWN, wait=0.2)    #追加（予備
                self.press(Button.A, wait=0.2)
                if self.isContainTemplate('InfinityUtil\year_max.png',threshold=0.9): 
                    # 2060対応
                    self.press(Direction.DOWN, duration=8, wait=0.5)
                else:
                    # 年アップ
                    self.press(Direction.UP, wait=0.2)
                self.press(Direction.RIGHT, duration=1, wait=0.3)
                self.press(Button.A, wait=0.5)
                self.press(Button.HOME, wait=1)  # ゲームに戻る
                self.press(Button.HOME, wait=2)

                self.press(Button.B, wait=1)
                self.press(Button.A, wait=1)  # レイドをやめる
                # エリアに戻るまで
                while not self.isContainTemplate('Network_Offline.png',threshold=0.9): 
                    self.wait(0.5)

                # コメント化
                #self.press(Button.A, wait=1)
                #self.press(Button.A, wait=1)  # 2000W
                #self.press(Button.A, wait=1.8)
                #self.press(Button.A, wait=1.8)  # 追加れいど開始
                #self.press(Button.B, wait=1.5)

                #self.press(Button.HOME, wait=1)
                #self.press(Direction.DOWN)
                #self.press(Direction.RIGHT)
                #self.press(Direction.RIGHT)
                #self.press(Direction.RIGHT)
                #self.press(Direction.RIGHT)
                #self.press(Direction.RIGHT) #追加
                #self.press(Button.A, wait=1.5)  # 設定選択
                #self.press(Direction.DOWN, duration=2, wait=0.5)
                #
                #self.press(Button.A, wait=0.3)  # 設定 > 本体
                #self.press(Direction.DOWN)
                #self.press(Direction.DOWN)
                #self.press(Direction.DOWN)
                #self.press(Direction.DOWN)
                #self.press(Direction.DOWN, wait=0.3)    #追加
                #self.press(Direction.DOWN, wait=0.3)    #追加
                #self.press(Direction.DOWN, wait=0.3)    #追加
                #self.press(Direction.DOWN, wait=0.3)    #追加
                #self.press(Button.A)  # 日付と時刻 選択
                #self.press(Direction.DOWN, duration=0.7, wait=0.2)    #追加
                #self.press(Button.A, wait=0.5)
                #
                #self.press(Button.HOME, wait=1)  # ゲームに戻る
                #self.press(Button.HOME, wait=1)

    # Controls the system time and get every-other-day bonus without any punishments
    def timeLeapMod(self, is_go_back=True):
        self.press(Button.HOME, wait=1)
        self.press(Direction.DOWN)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Direction.RIGHT)
        self.press(Button.A, wait=1.5)  # System Settings
        self.press(Direction.DOWN, duration=2, wait=0.5)

        self.press(Button.A, wait=0.3)  # System Settings > System
        self.press(Direction.DOWN)
        self.press(Direction.DOWN)
        self.press(Direction.DOWN)
        self.press(Direction.DOWN, wait=0.3)
        self.press(Direction.DOWN, wait=0.3)    #追加
        self.press(Direction.DOWN, wait=0.3)    #追加
        self.press(Direction.DOWN, wait=0.3)    #追加
        self.press(Direction.DOWN, wait=0.3)    #追加
        self.press(Button.A, wait=0.2)  # Date and Time
        self.press(Direction.DOWN, duration=0.7, wait=0.2)

        # increment and decrement
        if is_go_back:
            self.press(Button.A, wait=0.2)
            self.press(Direction.UP, wait=0.2)  # Increment a year
            self.press(Direction.RIGHT, duration=1.5)
            self.press(Button.A, wait=0.5)

            self.press(Button.A, wait=0.2)
            self.press(Direction.LEFT, duration=1.5)
            self.press(Direction.DOWN, wait=0.2)  # Decrement a year
            self.press(Direction.RIGHT, duration=1.5)
            self.press(Button.A, wait=0.5)

        # use only increment
        # for use of faster time leap
        else:
            self.press(Button.A, wait=0.2)
            self.press(Direction.RIGHT)
            self.press(Direction.RIGHT)
            self.press(Direction.UP, wait=0.2)  # increment a day
            self.press(Direction.RIGHT, duration=1)
            self.press(Button.A, wait=0.5)

        self.press(Button.HOME, wait=1)
        self.press(Button.HOME, wait=1)