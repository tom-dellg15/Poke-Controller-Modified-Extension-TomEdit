#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from Commands.Keys import Button
from Commands.PythonCommandBase import ImageProcPythonCommand


class MashA_Common(ImageProcPythonCommand):
    def  __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        
        self.count_max = 60
        self.wait_time_Eng = 0.9
        
     
    def Screen_Shot(self):
        self.camera.saveCapture()
        self.wait(1.0)

# 時間があれば処理を1つの関数に集約する

# Mash a button A
# A連打
class MashA_Fossilized_Drake(MashA_Common):
    NAME = '【剣盾】A連打（カセキのリュウ）'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        
    def do(self):
        # 時刻表示
        print(datetime.datetime.now())
        count = 0
        while True:
            self.wait(0.5)
            self.press(Button.A)
            ## test start
            #if self.isContainTemplate('Fossilized.png', threshold=0.9):
            #    self.Screen_Shot()
            ## test end
            if self.isContainTemplate('Fossilized_Drake.png', threshold=0.9):
                count += 1;
                print(str(count) + "個目の”カセキのリュウ”を発掘")
            if count + 1 > self.count_max:
                break
        # 時刻表示
        print(datetime.datetime.now())
        self.LINE_image("*** ”カセキのリュウ”発掘完了” ***") # LINE通知

# Mash a button A
# A連打
class MashA_Fossilized_Fish(MashA_Common):
    NAME = '【剣盾】A連打（カセキのサカナ）'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        
    def do(self):
        # 時刻表示
        print(datetime.datetime.now())
        count = 0
        while True:
            self.wait(0.5)
            self.press(Button.A)
            if self.isContainTemplate('Fossilized_Fish.png', threshold=0.9):
                count += 1;
                print(str(count) + "個目の”カセキのサカナ”を発掘")
            if count + 1 > self.count_max:
                break
        # 時刻表示
        print(datetime.datetime.now())
        self.LINE_image("*** ”カセキのサカナ”発掘完了” ***") # LINE通知

# Mash a button A
# A連打
class MashA_Fossilized_Drake_Eng(MashA_Common):
    NAME = '【剣盾】A連打（カセキのリュウ）(英語版)'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        

    def do(self):
        # 時刻表示
        print(datetime.datetime.now())
        count = 0
        while True:
            self.wait(0.5)
            self.press(Button.A)
            if self.isContainTemplate('Fossilized_Drake_Eng.png', threshold=0.9):
                count += 1;
                print(str(count) + "個目の”カセキのリュウ”を発掘")
                self.wait(self.wait_time_Eng)
                self.press(Button.A)
            if count + 1 > self.count_max:
                break
        # 時刻表示
        print(datetime.datetime.now())
        self.LINE_image("[Eng]*** ”カセキのリュウ”発掘完了” ***") # LINE通知

# Mash a button A
# A連打
class MashA_Fossilized_Fish_Eng(MashA_Common):
    NAME = '【剣盾】A連打（カセキのサカナ）(英語版)'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        

    def do(self):
        # 時刻表示
        print(datetime.datetime.now())
        count = 0
        while True:
            self.wait(0.5)
            self.press(Button.A)
            if self.isContainTemplate('Fossilized_Fish_Eng.png', threshold=0.9):
                count += 1;
                print(str(count) + "個目の”カセキのサカナ”を発掘")
                self.wait(self.wait_time_Eng)
                self.press(Button.A)
            if count + 1 > self.count_max:
                break
        # 時刻表示
        print(datetime.datetime.now())
        self.LINE_image("[Eng]*** ”カセキのサカナ”発掘完了” ***") # LINE通知