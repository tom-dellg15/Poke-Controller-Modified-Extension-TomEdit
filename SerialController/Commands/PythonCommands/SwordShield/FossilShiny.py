#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import ImageProcPythonCommand


class Fossil_shiny(ImageProcPythonCommand):
    def __init__(self, cam):
        super().__init__(cam)
        self.count = 0
        self.max = 30

    '''
    前提：手持ちは6匹にしておくこと！
    　　　6番道路のカセキ復元の人の前でレポートを書いておくこと
    head = {0 : "カセキのトリ", 1 : "カセキのサカナ"}
    body = {0 : "カセキのリュウ", 1 : "カセキのクビナガ"}
    lang = {J : "日本語", E : "英語"}
    '''
    def fossil_loop(self, head=0, body=0, lang="J"):
        # Bボタンを0.5秒間隔で5回押す
        self.pressRep(Button.B, repeat=5, interval=0.5)
        print(datetime.datetime.now())
        #start = time.time()
        i = 0
        while True:
            for j in range(self.max):
                print(str(self.max * i + j + 1) + "体目 (" + format(j + 1) + "/" + str(self.max) + " of a box)")
                if lang == "J":
                    self.press(Button.A, wait=0.75)
                    self.press(Button.A, wait=0.75)
                else:
                    self.press(Button.A, wait=1.0)
                    self.press(Button.A, wait=1.2)
                    
                if lang == "J":
                    if head == 1:
                        self.press(Direction.DOWN, duration=0.07, wait=0.75)  # select fossil
                    self.press(Button.A, wait=0.75)  # determine fossil

                    if body == 1:
                        self.press(Direction.DOWN, duration=0.07, wait=0.75)  # select fossil
                    self.press(Button.A, wait=0.75)  # determine fossil
                else:
                    if head == 1:
                        self.press(Direction.DOWN, duration=0.07, wait=0.75)  # select fossil
                    self.press(Button.A, wait=1.2)  # determine fossil

                    if body == 1:
                        self.press(Direction.DOWN, duration=0.07, wait=0.75)  # select fossil
                    self.press(Button.A, wait=1.2)  # determine fossil
                    
                self.press(Button.A, wait=0.5)  # select "それでよければ"
                while not self.isContainTemplate('Network_Offline.png', 0.8):
                    self.press(Button.B, wait=0.5)
                self.wait(1.0)

            # open up pokemon box
            self.press(Button.X, wait=1)
            self.press(Direction.RIGHT, duration=0.07, wait=1)
            self.press(Button.A, wait=2)
            self.press(Button.R, wait=2)

            is_contain_shiny = self.CheckBox(lang)
            # tm = round(time.time() - start, 2)
            # print('Loop : {} in {} sec. Average: {} sec/loop'.format(i, tm, round(tm / i, 2)))
            if is_contain_shiny:
                print('Shiny!')
                break

            self.press(Button.HOME, wait=2)  # EXIT Game
            self.press(Button.X, wait=0.6)
            self.press(Button.A, wait=2.5)  # closed
            self.press(Button.A, wait=2.0)  # Choose game
            self.press(Button.A)  # User selection
            # 起動チェック中
            while self.isContainTemplate("check_soft.png", threshold=0.9):
                #何もしない
                self.wait(0.5)
            while not self.isContainTemplate('OP.png', 0.7):  # recognize Opening
                self.wait(0.2)
            self.press(Button.A)  # load save-data
            while not self.isContainTemplate('Network_Offline.png', 0.8):
                self.wait(0.5)
            self.wait(1.0)
            i += 1
        print(datetime.datetime.now())

    def CheckBox(self,lang):
        row = 5
        col = 6
        for i in range(0, row):
            for j in range(0, col):
                # if shiny, then stop
                if self.isContainTemplate('shiny_mark.png', threshold=0.9):
                    if lang == "J":
                        self.LINE_image("*** ”色違い発見しました” ***") # LINE通知
                    else:
                        self.LINE_image("[Eng]*** ”色違い発見しました” ***") # LINE通知
                    return True
                # Maybe this threshold works for only Japanese version.
                if lang == "J":
                    if self.isContainTemplate('status.png', threshold=0.7):
                        pass
                else:
                    if self.isContainTemplate('status_Eng.png', threshold=0.7):
                        pass
                if not j == col - 1:
                    if i % 2 == 0:
                        self.press(Direction.RIGHT, wait=0.2)
                    else:
                        self.press(Direction.LEFT, wait=0.2)
            self.press(Direction.DOWN, wait=0.2)
        return False


class Fossil_shiny_00(Fossil_shiny):  # パッチラゴン
    NAME = '【剣盾】カセキ色厳選(パッチラゴン)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(0, 0)


class Fossil_shiny_01(Fossil_shiny):  # パッチルドン
    NAME = '【剣盾】カセキ色厳選(パッチルドン)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(0, 1)


class Fossil_shiny_10(Fossil_shiny):  # ウオノラゴン
    NAME = '【剣盾】カセキ色厳選(ウオノラゴン)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(1, 0)


class Fossil_shiny_11(Fossil_shiny):  # ウオチルドン
    NAME = '【剣盾】カセキ色厳選(ウオチルドン)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(1, 1)

class Fossil_shiny_Eng_00(Fossil_shiny):  # パッチラゴン
    NAME = '【剣盾】カセキ色厳選(パッチラゴン)(英語版)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(0, 0, "E")


class Fossil_shiny_Eng_01(Fossil_shiny):  # パッチルドン
    NAME = '【剣盾】カセキ色厳選(パッチルドン)(英語版)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(0, 1, "E")


class Fossil_shiny_Eng_10(Fossil_shiny):  # ウオノラゴン
    NAME = '【剣盾】カセキ色厳選(ウオノラゴン)(英語版)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(1, 0, "E")


class Fossil_shiny_Eng_11(Fossil_shiny):  # ウオチルドン
    NAME = '【剣盾】カセキ色厳選(ウオチルドン)(英語版)'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.fossil_loop(1, 1, "E")