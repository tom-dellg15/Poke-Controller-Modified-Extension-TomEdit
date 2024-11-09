import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE2_util import EXE2_util

class Exe2LocalBattleRealLoser(EXE2_util):
    NAME = '【EXE2】本番バトル_★敗者★'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用本番バトル敗者側のループ処理_v1.0 Release.2024/10/12
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
        self.winner_flag = False    #敗者
        self.host_flag = True   #True：ホスト側　False：クライアント側

        self.pvpBattle_count_max = 3000  # バトル最大回数
        # self.regular_Index = 1   # レギュラーチップ：バリアブルソード
        self.battle_count = 0
        self.logout_count = 0

    def do(self):
        self.EXExPrint(
            self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                + "▼▼▼本番バトル処理開始▼▼▼"
        )
        # 時刻表示
        self.EXExPrint(
            self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                + str(datetime.datetime.now())
        )
        # 初回メッセージ
        if self.pvpBattle_count_max > 0 :
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                    + str(self.pvpBattle_count_max) 
                    + "回 本番バトルを行います"
            )
        else:
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                    + "回数指定なしの為、本番バトル処理無限ループ開始"
            )
        while True :            
            #ネットワーク画面処理
            self.EXE2NetWorkMenu(self.host_flag, self.winner_flag)

            #リザルト画面判定
            self.EXE2PvpResult(self.winner_flag) 
            #エラー処理
            if self.sytem_code != self.normal_end :
                self.EXE2Error(True)
                break

            #リトライ処理判定
            self.EXE2PvpRetry(self.winner_flag)

            #カスタム画面処理（敗者）
            self.EXE2CustomScreenLoserLogic(self.winner_flag)
            self.init_flag = False
            
            #ドロー（タイムアウト）
            self.EXE2PvpResultDraw(self.winner_flag)

            #ドロー（ネットワークメニューに戻る）
            self.EXE2PvpResultToNetWorkMenu(self.winner_flag)
            
            #指定回数で終了する
            if self.pvpBattle_count_max > 0 :
                if self.battle_count >= self.pvpBattle_count_max :
                    # LINE通知
                    self.LINE_image(self.EXExGetSeriesTag(self.seriesNumber)
                        + self.EXExGetVictoryDefeatPlayer(self.winner_flag)
                        + "本番バトル処理終了："
                        + str(self.pvpBattle_count_max) + "回敗北") 
                    break

        self.EXExPrint(
            self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                + "▲▲▲本番バトル処理終了▲▲▲"
        )

