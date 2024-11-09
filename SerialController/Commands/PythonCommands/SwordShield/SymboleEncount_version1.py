#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick

class SymboleEncount_version1(ImageProcPythonCommand):
    NAME = '【剣盾】固定シンボル厳選_version1'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("-------------------------------")
        print("固定シンボル厳選_version1")
        print("Developed by ぽけ太")
        print("-------------------------------")
        print("start!!")
        self.wait(1)
        count = 1
        
        while True:
            print("現在", count, "回目")

            #ポケモン剣盾のソフトを起動する
            self.pressRep(Button.A, 5, interval=0.5)
            while not self.isContainTemplate('image_SymboleEncount/Opening.png', 0.7):
                self.wait(0.5)
            print("オープニングムービーをスキップしました")
            self.pressRep(Button.A, 5, interval=0.2)
            
            #「野生の◯◯が現れた」が表示されるまで待機
            while not self.isContainTemplate('image_SymboleEncount/PokemonAppearence.png', 0.7):
                self.wait(0.1)
            print("野生の◯◯が現れた")
            self.wait(2.7) #上記の表示からバトルコマンドの表示までの時間
            
            #色違いかどうかの判定(”エルレイド”表示までの時間差で判定)
            if self.isContainTemplate('image_SymboleEncount/Gallade.png', 0.7): 
                print("通常色です")
                self.press(Button.HOME, 0.1, 1)
                self.press(Button.X, 0.1, 0.5)
                self.press(Button.A, 0.1, 0.5)
                self.wait(3)
                if self.isContainTemplate('image_SymboleEncount/Hometime23.png', 0.9):  #"23:..."を認識したら0時台まで時間を戻す
                    self.timeleaping()
                count = count + 1
            else: #想定時間に”エルレイド”が表示されていない場合、色違いと判定
                print("色違いが出現しました！！(現在", count, "回目)")
                self.wait(0.2)
                #self.LINE_image("色違いが出ました!!") #LINE_Notify導入時はLINEにて通知可能(#を消す)
                break
    
    #日付を跨がないようにするための関数
    def timeleaping(self):
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
