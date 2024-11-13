#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

class AutoShinyPalkia(ImageProcPythonCommand):
    NAME = '【BDSP】パルキア厳選'

    def __init__(self,cam):
        super().__init__(cam)

    def do(self):
        print("-------------------------------")
        print("BDSP「パルキア」厳選【日本語版】")
        print("Developed by ますたー")
        print("See also ますたーの忘備録")
        print("URL: https://tangential-star.hatenablog.jp/ ")
        print("-------------------------------")
        self.wait(0.5)
        count = 1
        print("Start")

        while True:
            #フィールド
            print("上移動なう...")
            self.press(Direction.UP, 1.2, 0.1) 
            print("パルキア「ガギャギャァッ！！！」（", count, "回目）")

            #パルキア「ガギャギャァッ」待ち
            while not (self.isContainTemplate('BDSP_gagyagya.png', threshold=0.9, use_gray=True, show_value=False)):
                self.wait(0.1)
            self.wait(1.2) # 鳴き声待ち
            self.press(Button.A, 0.1,  0.3)  #Aを押してテキスト送り
            self.press(Button.A, 0.05, 0.02) #Aを押してテキスト送り（なぜか2回押さないと進まない謎仕様）

            #パルキアがあらわれた！ からエフェクト確認するために待機
            while not self.isContainTemplate('BDSP_arawareta_Palkia.png',0.8, show_value=False):
                self.wait(0.04)

            print("パルキアが現れた！（", count, "回目）")
            self.wait(2.4)

            #「いっておいで●●」もしくは「ゆけっ！」の場合は通常色
            if( self.isContainTemplate('BDSP_itteoide.png', threshold=0.9, use_gray=True, show_value=False) \
                or self.isContainTemplate('BDSP_yuke.png', threshold=0.9, use_gray=True, show_value=False)):

                #リセット
                print("通常色なのでリセットします（",count,"回目）")
                self.press(Button.HOME, 0.3, 1.2)
                self.press(Button.X,    0.3, 1.2) 
                self.press(Button.A,    0.3, 1.5) 

                #再起動
                print("再起動！")
                self.press(Button.A,    0.3, 1.5) 
                self.press(Button.A,    0.3, 1.2) 

                #パルキアのカウントを1増やす
                count += 1

                while not ( self.isContainTemplate('BDSP_yarinohashira.png', threshold=0.9, use_gray=True, show_value=False) \
                    or self.isContainTemplate('BDSP_yarinohashira_kanji.png', threshold=0.9, use_gray=True, show_value=False) ):
                    self.press(Button.A, 0.2, 0.1)  #タイトル送り（タイトルへ）

                #やりのはしらにもどってくる
                print("やりのはしら")


            #ずれた場合は「色違い」
            else:
                print("色違いがでました!!（", count, "回目）")
                while not (self.isContainTemplate('BDSP_command.png', threshold=0.9, use_gray=True, show_value=False)):
                    self.wait(0.2)
                self.press(Button.CAPTURE,3) #キャプチャー
                self.finish()


