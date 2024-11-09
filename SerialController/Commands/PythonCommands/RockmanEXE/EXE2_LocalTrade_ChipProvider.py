import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE2_util import EXE2_util

class EXE2LocalTradeChipProvider(EXE2_util):
    NAME = '【EXE2】ローカルトレード_チップ提供側'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用ローカルトレード（チップ提供側）のループ処理_v1.0 Release.2024/10/14
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

        self.host_flag = True   #True：ホスト側　False：ゲスト側
        self.debug_flag = True

        self.pvpTrade_count_max = 0  # トレード最大回数
        self.trate_count = 0

    def do(self):
        self.EXExPrint(
            "▼▼▼ローカルトレード（チップ提供側）開始▼▼▼"
        )
        # 時刻表示
        self.EXExPrint(
            str(datetime.datetime.now())
        )
        # 初回メッセージ
        if self.pvpTrade_count_max > 0 :
            self.EXExPrint(
                str(self.pvpTrade_count_max) 
                    + "回 トレードを行います"
            )
        else:
            self.EXExPrint(
                "回数指定なしの為、ローカルトレード処理無限ループ開始"
            )
        while True :            
            #ネットバトルにカーソルが当たっているとき
            templatePass = self.EXExGetTemplPass("_network_netbattle.png")
            if self.isContainTemplate(templatePass, threshold=0.98):
                #トレードにカーソルが当たるまで移動
                templatePass = self.EXExGetTemplPass("_network_trade.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    self.press(Hat.BTM, wait=0.1)
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "トレード選択"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)

            #パブリックトレードにカーソルが当たっているとき
            templatePass = self.EXExGetTemplPass("_network_publictrade.png")
            if self.isContainTemplate(templatePass, threshold=0.98):
                #ローカルトレードにカーソルが当たるまで移動
                templatePass = self.EXExGetTemplPass("_network_localtrade.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    self.press(Hat.BTM, wait=0.1)
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "ローカルトレード選択"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)
            
            #チップトレードにカーソルが当たっているとき
            templatePass = self.EXExGetTemplPass("_network_trade_chip.png")
            if self.isContainTemplate(templatePass, threshold=0.98):
                #チップトレードにカーソルが当たるまで移動
                templatePass = self.EXExGetTemplPass("_network_trade_chip.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    self.press(Hat.BTM, wait=0.1)
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "チップトレード選択"
                    , debug_flag=self.debug_flag
                )
                #ホスト選択★
                self.hostSelect()
                # self.wait(0.5)

            #Nextにカーソルが当たっているとき
            templatePass = self.EXExGetTemplPass("_network_trade_next.png")
            if self.isContainTemplate(templatePass, threshold=0.98):
                self.press(Button.A, wait=0.1)
                # self.wait(0.5)

            ####★任意のチップを自動でサーチするようにロジック化するか？★
            # #チップ選択画面に遷移したとき
            # templatePass = self.EXExGetTemplPass("_network_trade_chipselect.png")
            # if self.isContainTemplate(templatePass, threshold=0.98):
            #     self.wait(0.5)
            #     #何も選ばないにカーソルが当たるまで移動
            #     templatePass = self.EXExGetTemplPass("_network_trade_chipselect_nochip.png")
            #     while not self.isContainTemplate(templatePass, threshold=0.9):
            #         self.press(Hat.TOP, wait=0.1)
            #     self.press(Button.A, wait=0.5)
            #     self.EXExPrint(
            #         "何も選ばない"
            #         , debug_flag=self.debug_flag
            #     )
            #     self.wait(0.5)

            #メッセージ選択がでたとき
            templatePass = self.EXExGetTemplPass("_network_msgselect.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "コメント選択"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)

            #相手が見つからないとき
            templatePass = self.EXExGetTemplPass("_network_trade_communicationretry_no.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                #はいにカーソルが当たるまで移動してはい押下
                templatePass = self.EXExGetTemplPass("_network_trade_communicationretry_yes.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    self.press(Hat.TOP, wait=0.1)
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "・・・通信リトライ・・・"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)
            
            #プレイヤーが認識されたとき
            templatePass = self.EXExGetTemplPass("_network_playerlist_tradeshiyouyo.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                # self.wait(0.5)
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "プレイヤー選択"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)

            #トレード申込画面が表示されたとき
            templatePass = self.EXExGetTemplPass("_network_trade_request.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "トレード申込 -> 即開始"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)

            #トレードが成功したとき
            templatePass = self.EXExGetTemplPass("_network_trade_sccess.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                self.trate_count += 1
                self.press(Button.A, wait=0.5)
                self.EXExPrint(
                    "トレード成功！"
                    , debug_flag=self.debug_flag
                )
                # self.wait(0.5)

            #指定回数で終了する
            if self.pvpTrade_count_max > 0 :
                if self.trate_count >= self.pvpTrade_count_max :
                    # LINE通知
                    self.LINE_image(self.EXExGetSeriesTag(self.seriesNumber)
                        + "ローカルトレード（チップ提供側）終了："
                        + str(self.pvpTrade_count_max) + "回トレード完了") 
                    break

        self.EXExPrint(
            "▲▲▲ローカルトレード（チップ提供側）終了▲▲▲"
        )

    def hostSelect(self):
        #ホスト選択
        templatePass = self.EXExGetTemplPass("_network_trade_host.png")
        if self.isContainTemplate(templatePass, threshold=0.98):
            #ホストにカーソルが当たるまで移動
            templatePass = self.EXExGetTemplPass("_network_trade_host.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.press(Hat.BTM, wait=0.1)
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                "ホスト選択"
                , debug_flag=self.debug_flag
            )
