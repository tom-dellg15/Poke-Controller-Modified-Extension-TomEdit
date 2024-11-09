#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick

class WildEncount_version1(ImageProcPythonCommand):
    NAME = '【剣盾】野生厳選'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("-------------------------------")
        print("野生厳選")
        print("Developed by ぽけ太")
        print("-------------------------------")
        print("start!!")
        self.wait(1)
        count = 1
        self.press(Button.B, 0.1, 0.1)

        while True:
            print("現在", count, "回目")

            #ポケモンに遭遇するまで移動する
            self.press(Button.LCLICK, 0.1, 1) #ねらうポケモンによって変更する
            self.hold(Direction(Stick.LEFT, 110, 1), wait=0.15)
            self.hold(Direction(Stick.RIGHT, 15, 1))
            while not self.isContainTemplate('image_WildEncount/PokemonAppearence.png', 0.7):
                self.wait(0.1)
            self.holdEnd([Direction(Stick.RIGHT, 15), Direction(Stick.LEFT, 110)])

            print("野生の◯◯が現れた")
            self.wait(2.5) #上記の表示からバトルコマンドの表示までの時間

            #色違いかどうかの判定(”エルレイド”表示までの時間差で判定)
            if self.isContainTemplate('image_WildEncount/Gallade.png', 0.7): 
                print("通常色です")
                while not self.isContainTemplate('image_WildEncount/battle_escape.png', 0.7):
                    self.wait(0.1)
                self.press(Hat.TOP, 0.1, 0.5)
                self.press(Button.A, 0.1, 0.1)
                while not self.isContainTemplate('image_WildEncount/escape_success.png', 0.7):
                    self.wait(0.1)
                self.wait(4)
                self.press(Button.HOME, 0.1, 0.75)
                if self.isContainTemplate('image_WildEncount/HomeTime23.png', 0.92): #23時を認識したら0時まで戻す
                     self.press(Button.HOME, 0.1, 1)
                     self.CampTimeLeap()
                     count = count + 1
                     while not self.isContainTemplate('image_WildEncount/blackback.png', 0.7):
                        self.wait(0.1)              
                else:
                    self.press(Button.HOME, 0.1, 0.5)
                    count = count + 1
            
            else: #想定時間に”エルレイド”が表示されていない場合、色違いと判定
                print("色違いが出現しました！！(現在", count, "回目)")
                self.LINE_image("色違いが出ました!!") #LINE_Notify導入時はLINEにて通知可能(#を消す)
                break

    def CampTimeLeap(self):
        print("時間を戻します")

        #メニューからキャンプを選択（キャンプコマンドは左上に設置する）
        self.press(Button.X, 0.1, 1)
        self.press(Button.A, 0.1, 0.1)
        while not self.isContainTemplate('image_WildEncount/Camp_menu.png', 0.7):
            self.wait(0.1)
        self.wait(0.5)

        #時間を戻す
        self.press(Button.HOME, 0.1, 1)
        self.press(Hat.BTM, 0.1, 0.1)
        self.pressRep(Hat.RIGHT, 5, 0.1)
        self.press(Button.A, 0.1, 1)
        self.pressRep(Hat.BTM, 16, 0.1)
        self.press(Button.A, 0.1, 0.5)
        self.pressRep(Hat.BTM, 9, 0.1)
        self.press(Button.A, 0.1, 0.5)
        self.pressRep(Hat.BTM, 2, 0.1)
        self.press(Button.A, 0.1, 0.5)
        self.pressRep(Hat.RIGHT, 3, 0.1)
        self.pressRep(Hat.BTM, 23, 0.1) #真ん中の引数(23)で巻き戻す時間の指定
        self.pressRep(Button.A, 3, 0.1)
        self.press(Button.HOME, 0.1, 1)
        self.press(Button.HOME, 0.1, 1)

        #キャンプをやめる
        self.wait(1)
        self.press(Button.B, 0.1, 0.5)
        self.press(Button.A, 0.1, 0.1)

            

