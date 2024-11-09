import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from .EXE2_util import EXE2_util

class Exe2LocalBattleRealWinner(EXE2_util):
    NAME = '【EXE2】本番バトル_☆勝者☆'
    '''
    --------------------------------------------------------------------------------------
     EXE2専用本番バトル勝者側のループ処理_v1.0 Release.2024/10/12
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
        self.winner_flag = True #勝者
        self.host_flag = False   #True：ホスト側　False：クライアント側

        self.pvpBattle_count_max = 3000  # バトル最大回数
        self.regular_Index = 1   # レギュラーチップ：バリアブルソード
        self.battle_count = 0
        self.logout_count = 0
        self.battle_count_coefficient = 1

    def do(self):
        self.EXExPrint(
            self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                + "▽▽▽本番バトル処理開始▽▽▽"
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

            #リトライ処理判定
            self.EXE2PvpRetry(self.winner_flag)

            #カスタム画面処理（勝者）
            chipArray = [
                            "_chip_customsword.png"
                            , "_chip_varswrd.png" 
                            , "_chip_protomanV3.png"
                        ]
            self.EXE2CustomScreenWinnerLogic(self.winner_flag, chipArray, self.regular_Index)
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
                        + str(self.pvpBattle_count_max) + "回勝利") 
                    break
            #途中経過報告(4回に分けて通知)
            if self.battle_count  == ( self.pvpBattle_count_max // 4 ) * self.battle_count_coefficient :
                self.battle_count_coefficient += 1
                # LINE通知
                self.LINE_image(self.EXExGetSeriesTag(self.seriesNumber)
                    + self.EXExGetVictoryDefeatPlayer(self.winner_flag)
                    + "本番バトル処理終了："
                    + str(self.battle_count) + "回勝利") 

        self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(self.winner_flag) 
                    + "△△△本番バトル処理終了△△△"
        )


