import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE3_util import EXE3_util

class EXE3BeatupGutsman(EXE3_util):
    NAME = '【EXE3】ガッツマンしばき'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用リセット処理_v1.0 Release.2024/10/22
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

        self.debug_flag = True
        self.count_flag = False

        self.count = 0
        self.linealarm_count = 100

    def do(self):
        self.EXExPrint(
            "▼▼▼ガッツマンしばき▼▼▼"
        )
        # 時刻表示
        self.EXExPrint(
            str(datetime.datetime.now())
        )

        """
        前提：レギュラーチップをデスマッチ２にしておく
        　　　ナビカスタマイザーでバスターＭＡＸをバグらせておく
        　　　これにより選択したチップが勝手に使用されるバグ発生
        """
        # 初回メッセージ
        self.EXExPrint( "【ガッツマンしばき】処理を開始します。" + str(self.linealarm_count) + "回おきにLINE通知します。"
            , line_flag=True
            , debug_flag=False
        )

        while True :
            # 基本Ａボタン連打
            self.press(Button.A, wait=0.2)

            # ナビカス画面になったとき
            templatePass = self.EXExGetTemplPass("_battlescreen_start_blue.png")
            if self.isContainTemplate(templatePass, threshold=0.7):
                # 一時的にコメントアウト（ガッツスタイルチェンジ稼ぎのため）
                # レギュラーチップ選択
                self.press(Button.A, wait=0.1)
                # OK選択
                self.press(Button.PLUS, wait=0.1)
                self.press(Button.A, wait=0.1)
                # リザルト画面になるまで
                templatePass = self.EXExGetTemplPass("_result.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    # バスター連打
                    self.press(Button.B, wait=0.1)
                self.count += 1
                self.count_flag = True
                # １０回ごとにログ出力
                if ( self.count % 10 == 0) :
                    self.EXExPrint(
                        str(self.count) + "回到達。"
                    )
            
            # デカオにネットバトルもうしこむ？になったとき
            templatePass = self.EXExGetTemplPass("_msg_battle_request_dekao.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                # はいになるまで
                templatePass = self.EXExGetTemplPass("_msg_battle_request_dekao_yes.png")
                while not self.isContainTemplate(templatePass, threshold=0.9):
                    # 左
                    self.press(Hat.LEFT, wait=0.5)
            
            # self.line_count回ごとにLINE通知
            if ( self.count_flag and self.count % self.linealarm_count == 0) :
                self.count_flag = False
                # 時刻表示
                self.EXExPrint(
                    str(datetime.datetime.now())
                )
                self.EXExPrint(str(self.count) + "回に到達しました。"
                    , line_flag=True
                    , debug_flag=False
                )

            # PET画面になったとき
            templatePass = self.EXExGetTemplPass("_pet_secreen.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                # ループ終了
                break

        self.EXExPrint(
            "▲▲▲ガッツマンしばき▲▲▲"
        )

