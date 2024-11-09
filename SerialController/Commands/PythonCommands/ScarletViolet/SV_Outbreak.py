#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright (c) 2022 ぽけ太のゲーム部屋
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick
import tkinter as tk
import tkinter.ttk as ttk
import os
import glob

class SV_Outbreak(ImageProcPythonCommand):
    NAME = '【ＳＶ】大量発生厳選'

    global path_list, Outbreak_list, selected_pokemon
    path_list = []
    Outbreak_list = []
    selected_pokemon = None

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("--------------------------------------------------------------")
        print("SV_大量発生厳選")
        print("Developed by ぽけ太")
        print("--------------------------------------------------------------")
        print("start!!")
        self.makelist()
        self.SelectDialog()
        while selected_pokemon == None:
            self.wait(0.1)
        if selected_pokemon == "":
            print("厳選する大量発生を選択してください")
        else:  
            self.selected_path = "image_SV_Outbreak/" + selected_pokemon + ".png"
            print(selected_pokemon+"を狙います")
            while True:
                self.wait(2)
                if self.isContainTemplate(self.selected_path, 0.6):
                    print("大量発生を確認しました")
                    self.LINE_image("大量発生を確認しました") #LINE_Notify導入時はLINEにて通知可能(#を消す)
                    break
                else:
                    self.press(Button.HOME, 0.1, 1)
                    self.press(Hat.LEFT, 0.1, 0.1)
                    self.press(Hat.BTM, 0.1, 0.1)
                    self.press(Hat.LEFT, 0.1, 0.1)
                    self.press(Button.A, 0.1, 1)
                    self.pressRep(Hat.BTM, 16, 0.1,0.025)
                    self.press(Button.A, 0.1, 0.5)
                    self.pressRep(Hat.BTM, 9, 0.1)
                    self.press(Button.A, 0.1, 0.5)
                    self.pressRep(Hat.BTM, 2, 0.1)
                    self.press(Button.A, 0.1, 0.5)
                    self.pressRep(Hat.RIGHT, 4, 0.1)
                    self.press(Hat.BTM, 0.1, 0.1)
                    self.pressRep(Button.A, 2, 0.1)
                    self.pressRep(Button.HOME, 2, 0.1, 1)

    #画像ファイルを取得する関数
    def makelist(self):
        global path_list, Outbreak_list
        self.image_path = "./Template/image_SV_Outbreak/*.png"
        self.path_list = glob.glob(self.image_path) 
        Outbreak_list = [os.path.splitext(os.path.basename(file))[0] for file in self.path_list]
        
    #ダイアログを生成する関数
    def SelectDialog(self):
        self.SelectWindow = tk.Toplevel()
        self.SelectWindow.geometry("300x150")
        self.SelectWindow.title('大量発生厳選')
        self.frame = tk.Frame(self.SelectWindow)
        self.frame.pack()
        self.create_widgets()

    #ウィジェットを生成する関数
    def create_widgets(self):
        global Outbreak_list
        self.label = tk.Label(self.frame, text='ポケモンを選択してください')
        self.combobox = ttk.Combobox(self.frame, value=Outbreak_list)
        self.button = tk.Button(self.frame, text='OK', command=self.button_click)
        self.label.pack()
        self.combobox.pack()
        self.button.pack()

    #ボタンを押した時の処理
    def button_click(self):
        global selected_pokemon
        try:
            selected_pokemon = self.combobox.get()
        except:
            selected_pokemon = ""
        self.SelectWindow.destroy()
    

    



    