#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat


class BoxHatching_pkmnSWSH_Eng(ImageProcPythonCommand):
    NAME = '【剣盾】ボックス内卵孵化（英語版）'

    '''
    --------------------------------------------------------------------------------------
     前提：
     １）ボックス内の卵は左上から縦方向（列）に向かって、配置しておくこと
     　→処理としてはボックス内にある卵が何列存在するか、
     　　列内に卵が何個あるかチェックしています
     ２）実行前は自転車に乗っておくこと
     ３）場所はハシノマ原っぱで開始すること
     ４）手持ちは1匹にしておき、ほのおのからだなどの特性を持ったポケモンにしておくこと
     ５）開始前に孵化したい卵があるBOX数を必ず確認し指定すること
     ６）卵があるボックスを最初に開くようにしておくこと
     ７）複数ボックスの卵を孵化する場合は隣り合わせにしておき、
     　一番左にある卵ボックスを最初に開くようにしておくこと
    --------------------------------------------------------------------------------------
    '''
    def __init__(self, cam):
        super().__init__(cam)
        self.hatched_num = 0
        # self.count = 5
        self.place = 'wild_area'
        
        self.debug = False                      # debug用 True=デバッグようメッセージを出力
        self.box_max = 1                        # 孵化したい卵があるBOX数
        self.egg_row = 0                       # 処理中ボックス内に卵が何列分あるか
        self.egg_max = 0                       # BOX内にある孵化したい卵の数
        self.egg_on_hand = 0                       # 手持ち卵数
        self.egg_box_count = 0                # 卵孵化した1ボックス合計
        self.egg_total = 0                # 卵孵化した総合計
        # ボックスに置くときの列位置
        self.box_line = 0
        
    def do(self):
        # 時刻表示
        print(datetime.datetime.now())
        # ログ出力
        print("▼" + str(self.box_max) + "ボックス分の孵化作業を行います")
        # repeat A ゲーム起動直後にコマンド実行してもいいようにする
        while not self.isContainTemplate("Network_Offline.png", threshold=0.9):
            self.press(Button.A, wait=3.0)
        # 起動時に1度だけ行われる処理 #
        self.setup()
        # 指定したBOX数分繰り返す
        for box_count in range(1, self.box_max + 1):
            print(str(box_count) + "ボックス目 開始" )
            # クリア
            self.box_line = 0
            self.egg_row = 0
            self.egg_box_count = 0
            # ボックス内の卵をすべて孵化するまで繰り返す
            #while self.egg_box_count < self.egg_max:
            while True:
                self.wait(0.5)
                # ボックスに置くときの列位置
                self.box_line += 1
                # ポケモン選択
                self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
                self.press(Button.A, wait=2)
                # ボックスを開く
                self.press(Button.R, wait=2)
                # ボックス内卵列数カウント（当該ボックス初回だけ）
                if self.egg_row == 0:
                    # 一回左移動
                    self.press(Direction.LEFT, wait=0.2)
                    for i in range(0, 6):
                        self.press(Direction.RIGHT, wait=0.5)
                        if self.isContainTemplate("egg_status_Eng.png", threshold=0.9):
                            self.egg_row += 1
                    print("  box_count：" + str(box_count) + " egg_row：" + str(self.egg_row))
                    # 一度ボックスを閉じ
                    self.press(Button.B, wait=2.5)
                    # また開く
                    self.press(Button.R, wait=2)
                # 一回左移動
                self.press(Direction.LEFT, wait=0.2)
                # Multiselect
                self.press(Button.Y, wait=0.3)
                self.press(Button.Y, wait=0.3)
                # セル右移動（指定数分）
                for i in range(0, self.box_line):
                    self.press(Direction.RIGHT, wait=1)
                # Multiselect Start
                self.press(Button.A, wait=0.3)
                # セル下移動
                for i in range(0, 4):
                    self.press(Direction.DOWN, wait=0.3)
                # Multiselect End
                self.press(Button.A, wait=0.3)
                # 左移動（選択中）（指定数分）
                for i in range(0, self.box_line):
                    self.press(Direction.LEFT, wait=0.2)
                # 下移動
                self.press(Direction.DOWN, wait=0.3)
                # ドロップ
                self.press(Button.A, wait=0.3)
                # ボックスを閉じる
                self.press(Button.B, wait=2.5)
                # 手持ち卵の数をカウント
                self.egg_on_hand = 0
                for i in range(0, 5):
                    self.press(Direction.DOWN, wait=0.7)
                    if self.isContainTemplate("on_hand_egg_Eng.png", threshold=0.9):
                        self.egg_on_hand += 1
                    else:
                        break
                print("    egg_on_hand：" + str(self.egg_on_hand) + "（" + str(self.box_line) + "／" + str(self.egg_row) + "）")
                # ポケモンを閉じる
                self.press(Button.B, wait=1.5)
                self.press(Hat.LEFT, duration=0.1 , wait=0.5)   # set cursor to map
                # 空を飛ぶ（位置情報リセット）
                self.moveToInitialPlayerPosition()
                # 手持ちの卵が孵化し終わるまで（self.egg_on_hand分）
                self.Hatching()
                self.wait(2)
                # ボックスに預ける
                self.sendHatchedPokemonToBox(self.box_line)
                # ボックスがいっぱいになったら、次のボックスに移動させる
                if self.box_line == self.egg_row and box_count < self.box_max:
                    print("・・・次のボックスに移動・・・")
                    self.press(Hat.TOP, duration=0.1 ,wait=0.5)
                    self.press(Hat.RIGHT, duration=0.1, wait=0.5)
                # ボックスを閉じる
                self.press(Button.B, wait=0.5)  # ボックスが空でなかった場合でも、ボックスを閉じてループを実行し続けさせるのに必要な記述
                self.press(Button.B, wait=1.5)
                self.press(Button.B, wait=1.3)
                # メニュー画面のカーソルをタウンマップに戻す
                self.press(Hat.LEFT, duration=0.1 , wait=0.5)
                # 終了判定
                if self.box_line == self.egg_row:
                    print(str(box_count) + "ボックス目 完了。孵化数：" + str(self.egg_box_count))
                    break
        # 時刻表示
        print(datetime.datetime.now())
        # 総合計をログ出力　
        print("▲" + "孵化作業完了。孵化総合計：" + str(self.egg_total))
        self.LINE_image("[Eng]*** 孵化作業完了。孵化総合計：" + str(self.egg_total) + " ***") # LINE通知
    
    # 手持ちの卵孵化
    def Hatching(self):
        # クリア
        self.hatched_num = 0
        # 手持ちの卵数分（self.egg_on_hand分）処理する
        while self.hatched_num < self.egg_on_hand:
            # 卵が0個の時は右に1秒移動
            if self.hatched_num == 0:
                self.press(Direction.RIGHT, duration=1)
            # グルグル回る固定
            self.hold([Direction.RIGHT, Direction.R_LEFT])
            # 卵孵化メッセージが出るまでそのまま
            while not self.isContainTemplate('egg_notice_Eng.png'):
                self.wait(1)
            # 固定解除
            self.holdEnd([Direction.RIGHT, Direction.R_LEFT])
            # 画面が切り替わるまで
            while not self.isContainTemplate("Network_Offline.png", threshold=0.9):
                self.press(Button.A, wait=3.0)
            # 手持ちの卵孵化数をカウント
            self.hatched_num += 1
            print('      hatched_num: ' + str(self.hatched_num))
            # 卵が孵化した数
            self.egg_box_count += 1

    # デバッグ用メッセージ出力
    def debugMessage(self,methodName):
        #debug_message
        if self.debug:
            print("_method(AutoHatching_pkmnSWSH)_" + methodName)

    # 起動時に1度だけ行われる処理
    def setup(self):
        #debug_message
        self.debugMessage("setup")
        # Bボタンを0.5秒間隔で5回押す
        self.pressRep(Button.B, repeat=5, interval=0.5)
        # 認識したら、メニューの左上にカーソルを持っていく
        self.press(Button.X, wait=0.6)
        self.press(Hat.TOP_LEFT, 1.0, wait=0.8)

    # 空飛ぶタクシーでハシノマはらっぱに移動する関数
    # タウンマップにカーソルが当たっていることが前提
    def moveToInitialPlayerPosition(self):
        #debug_message
        self.debugMessage("moveToInitialPlayerPosition")
        self.press(Button.A, wait=3.0)
        self.pressRep(Button.A, repeat=2, interval=1.0)
        # 天候によって読み込み時間がやや異なる(最も重かった砂嵐でも1900で安定していたが、柱の本数や服装などの環境による差異がある可能性も考慮して少し余裕を持たせた)
        self.wait(2.2)

    # ボックスに預ける処理を呼び出す
    def sendHatchedPokemonToBox(self,box_line):
        #debug_message
        self.debugMessage("sendHatchedPokemonToBox")
        # メニューを開くよ
        self.press(Button.X, wait=1)
        # ポケモン選択
        self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
        self.press(Button.A, wait=2)
        # ボックスを開く
        self.press(Button.R, wait=2)

        # 手持ちの孵化したポケモンを範囲選択
        self.press(Hat.LEFT, duration=0.1, wait=0.5)
        self.press(Hat.BTM, duration=0.1, wait=0.5)
        self.press(Button.Y, wait=0.5)
        self.press(Button.Y, wait=0.5)
        self.press(Button.A, wait=0.5)
        self.press(Hat.BTM, duration=0.8, wait=0.5)
        self.press(Button.A, wait=0.5)
        
        # ボックスに移動させる
        self.pressRep(Hat.RIGHT, repeat=box_line, interval=0.5, wait=0.5)
        self.press(Hat.TOP, duration=0.1 ,wait=0.5)
        self.press(Button.A, wait=1.0)

