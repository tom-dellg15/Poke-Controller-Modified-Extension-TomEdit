import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE2_util import EXE2_util

class EXE2_ChipTrader(EXE2_util):
    NAME = '【EXE2】チップトレーダー'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用チップトレーダー処理_v1.0 Release.2024/10/16
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

        self.init_flag = True
        self.debug_flag = False
        self.line_flag = False
        
        self.get_asterisk_count_max = 0 # ＊チップが指定枚数欲しい場合に1以上を指定
        self.chipTrader_count_max = 5   # 何回チップトレーダ―を回すか指定する。1以上を指定すること
        self.count = 0
        self.wk_count = 0
        self.get_asterisk_count = 0

    def do(self):
        self.EXExPrint(
            "▼▼▼チップトレーダー開始▼▼▼"
        )
        # 時刻表示
        self.EXExPrint(
            str(datetime.datetime.now())
        )       

        while True : 
            if self.get_asterisk_count_max > 0:
                # 初回処理
                if self.init_flag :
                    # 初回メッセージ
                    self.EXExPrint(
                        "ガチャ最大回数："
                        + str(self.get_asterisk_count_max) + "個の＊チップがでるまで"
                    )
                # ＊チップを指定枚数引くまで
                self.gacharange(self.get_asterisk_count_max)
                #指定回数で終了する
                if self.get_asterisk_count >= self.get_asterisk_count_max :
                    # LINE通知
                    self.EXExPrint(self.EXExGetSeriesTag(self.seriesNumber)
                        + "チップトレーダ―："
                        + str(self.count) + "回まわして、"
                        + str(self.get_asterisk_count) + "個の＊チップが排出されました。"
                        , debug_flag=self.debug_flag
                        , line_flag=self.line_flag
                    ) 
                    break
            else:
                # 初回処理
                if self.init_flag :
                    # 初回メッセージ
                    self.EXExPrint(
                        "ガチャ最大回数："
                        + str(self.chipTrader_count_max) + "回まわすまで"
                    )
                # ＊指定回数ガチャを回すまで
                self.gacharange(self.chipTrader_count_max)
                #指定回数で終了する
                if self.count >= self.chipTrader_count_max :
                    # LINE通知
                    self.EXExPrint(self.EXExGetSeriesTag(self.seriesNumber)
                        + "チップトレーダ―："
                        + str(self.count) + "回まわして、"
                        + str(self.get_asterisk_count) + "個の＊チップが排出されました。"
                        , debug_flag=self.debug_flag
                        , line_flag=self.line_flag
                    ) 
                    break

        # Bボタン離す
        self.holdEnd(Button.B)

        self.EXExPrint(
            "▲▲▲チップトレーダー終了▲▲▲"
        )


    def gacharange(self, count_max):
        # チップトレーダ―スペシャルがあるバトルチップを10枚入れてみますか？
        templatePass = self.EXExGetTemplPass("_chiptrader_start_10.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            # はい
            self.press(Button.A, wait=0.5)
            # self.EXExPrint("チップトレーダ―スペシャルがあるバトルチップを10枚入れてみますか？",debug_flag=True)

        # コード＊のチップをゲットした場合　★順番考える
        templatePass = self.EXExGetTemplPass("_chiptrader_get_asterisk.png")
        if self.isContainTemplate(templatePass, threshold=0.98):
            if not ( self.wk_count == self.count ):
                self.wk_count = self.count
                self.get_asterisk_count += 1
                # LINE通知
                self.LINE_image(self.EXExGetSeriesTag(self.seriesNumber)
                    + "＊チップがチップトレーダから排出されました") 

        # 熱斗は、・・・をゲットした！！
        templatePass = self.EXExGetTemplPass("_chiptrader_get.png")
        if self.isContainTemplate(templatePass, threshold=0.9):        
            self.press(Button.A, wait=0.5)
            # self.EXExPrint("熱斗は、・・・をゲットした！！", debug_flag=self.debug_flag)

        # もういちどやりますか？
        templatePass = self.EXExGetTemplPass("_chiptrader_again_yes.png")
        if self.isContainTemplate(templatePass, threshold=0.9):        
            # はい
            self.press(Button.A, wait=0.5)
            # self.EXExPrint("もういちどやりますか？", debug_flag=self.debug_flag)

        # リュックの中
        templatePass = self.EXExGetTemplPass("_chiptrader_inbackoack.png")
        if self.isContainTemplate(templatePass, threshold=0.9):        
            # この10枚でよろしいですか？がでるまで
            templatePass = self.EXExGetTemplPass("_chiptrader_inbackoack_selected10.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):    
                # チップ選択
                self.press(Button.A, wait=0.1)
            # はい
            self.press(Button.A, wait=0.5)
            # self.EXExPrint("リュックの中,チップ選択,はい", debug_flag=self.debug_flag)

        # ゴトン！
        templatePass = self.EXExGetTemplPass("_chiptrader_goton.png")
        if self.isContainTemplate(templatePass, threshold=0.9):        
            self.count += 1
            self.press(Button.A, wait=0.5)
            # self.EXExPrint("ゴトン！", debug_flag=self.debug_flag)

        # 初回処理
        if self.init_flag :
            self.init_flag = False
            # Bボタン押し続ける
            self.hold(Button.B)
