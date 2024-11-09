#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick
import tkinter as tk

class SymboleEncount_version2(ImageProcPythonCommand):
    NAME = '【剣盾】固定シンボル厳選version2～時間帯に関する証'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("----------------------------------")
        print("固定シンボル厳選～時間帯に関する証")
        print("Developed by ぽけ太")
        print("----------------------------------")
        print("start!!")
        self.SelectDialog()
        global num
        if num == 4:
            self.finish()
        self.wait(1)
        count = 1
        
        while True:
            print("現在", count, "回目")

            #ポケモン剣盾のソフトを起動する
            self.pressRep(Button.A, 5, interval=0.5)
            while not self.isContainTemplate('image_SymboleEncount/Opening.png', 0.7):
                self.wait(0.5)
            print("オープニングムービーをスキップしました")
            self.pressRep(Button.A, 5, interval=0.3)
            
            #「野生の◯◯が現れた」が表示されるまで待機
            while not self.isContainTemplate('image_SymboleEncount/PokemonAppearence.png', 0.7):
                self.wait(0.1)
            print("野生の◯◯が現れた")
            self.wait(2.5) #上記の表示からバトルコマンドの表示までの時間
            
            #色違いかどうかの判定(”エルレイド”表示までの時間差で判定)
            if self.isContainTemplate('image_SymboleEncount/Gallade.png', 0.7): 
                print("通常色です")
                self.press(Button.HOME, 0.1, 1)
                self.press(Button.X, 0.1, 0.5)
                self.press(Button.A, 0.1, 0.5)
                self.wait(3)
                if num == 0: #しょうごの証を狙っている場合
                    if self.isContainTemplate('image_SymboleEncount/HomeTime19.png', 0.9):  #"19:..."を認識したら12時台まで時間を戻す
                        self.timeleaping()
                elif num == 1: #たそがれの証を狙っている場合
                    if self.isContainTemplate('image_SymboleEncount/HomeTime20.png', 0.9):  #"20:..."を認識したら19時台まで時間を戻す
                        self.timeleaping()
                elif num == 2: #しょうしの証を狙っている場合
                    if self.isContainTemplate('image_SymboleEncount/HomeTime6.png', 0.9):  #"6:..."を認識したら0時台まで時間を戻す
                        self.timeleaping()
                else: #あかつきの証を狙っている場合
                    if self.isContainTemplate('image_SymboleEncount/HomeTime12.png', 0.9):  #"12:..."を認識したら6時台まで時間を戻す
                        self.timeleaping()
                count = count + 1
            else: #想定時間に”エルレイド”が表示されていない場合、色違いと判定
                print("色違いが出現しました！！(現在", count, "回目)")
                #self.LINE_image("色違いが出ました!!") #LINE_Notify導入時はLINEにて通知可能(#を消す)
                break
    
    #日付変更の関数
    def timeleaping(self):
        global num
        print("時間を戻します")
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
        if num == 0: #しょうごの証を狙っている場合
            self.pressRep(Hat.BTM, 7, 0.1) 
        elif num == 1: #たそがれの証を狙っている場合
            self.pressRep(Hat.BTM, 1, 0.1) 
        elif num == 2: #しょうしの証を狙っている場合
            self.pressRep(Hat.BTM, 6, 0.1) 
        elif num == 3: #あかつきの証を狙っている場合
            self.pressRep(Hat.BTM, 6, 0.1) 
        self.pressRep(Button.A, 3, 0.1)
        self.press(Button.HOME, 0.1, 1)

    def SelectDialog(self):

        #メインウインドの作成
        root = tk.Tk()
        root.geometry('300x200')
        root.title('目的の証を選択')

        #ボタンクリック時に使用される関数
        def BtnClick1():
            global num
            num = 0
            print(str('”しょうごの証(12:00~18:59)”を狙います'))
            root.destroy()
        def BtnClick2():
            global num
            num = 1
            print(str('”たそがれの証(19:00~19:59)”を狙います'))
            root.destroy()
        def BtnClick3():
            global num
            num = 2
            print(str('”しょうしの証(20:00~05:59)”を狙います'))
            root.destroy()
        def BtnClick4():
            global num
            num = 3
            print(str('”あかつきの証(06:00~11:59)”を狙います'))
            root.destroy()
        def ClickClose():
            global num
            num = 4
            root.destroy()

        #各種ボタンの設置
        Btn1 = tk.Button(root, text='しょうごの証(12:00~18:59)', width=25, height=2, command=BtnClick1)
        Btn1.place(x=50, y=20)
        Btn2 = tk.Button(root, text='たそがれの証(19:00~19:59)', width=25, height=2, command=BtnClick2)
        Btn2.place(x=50, y=65)
        Btn3 = tk.Button(root, text='しょうしの証(20:00~05:59)', width=25, height=2, command=BtnClick3)
        Btn3.place(x=50, y=110)
        Btn4 = tk.Button(root, text='あかつきの証(06:00~11:59)', width=25, height=2, command=BtnClick4)
        Btn4.place(x=50, y=155)

        root.protocol("WM_DELETE_WINDOW", ClickClose)
        root.mainloop()