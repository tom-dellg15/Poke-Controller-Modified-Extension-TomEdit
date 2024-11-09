import time
import datetime

from .SWSH_util_box import SWSH_util_box
#from Commands.PythonCommands.ScarletViolet.SV_util_picnic import SV_util_picnic
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat

class AutoHatching_pkmnSWSH(SWSH_util_box):
    NAME = '【剣盾】自動リリース(英語版)'
    '''
    --------------------------------------------------------------------------------------
     自動逃がす(剣盾)_v1.0 Release.2024/4/13
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
        """ 
        ◆◆◆使用前に設定を確認してください◆◆◆
        """
        # 通知設定
        self.use_LINEnotice = True              # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになります True
        self.debug = True                       # debug用 True=デバッグようメッセージを出力
        # 色違い発見数
        self.shiny_count = 0

    def do(self):   
        '''
        /**
         * 育て屋から卵を回収→孵化→ボックスに預けるを繰り返すスケッチ
         * ボックスに空きがある限り、ポケモンを孵化し続ける
         *
         * 初期条件は以下の通り
         * 1.ハシノマはらっぱにいること
         * 1.対象ボックス内は逃がしたいポケモンだけにすること
         * 4.Xボタンを押したときに「タウンマップ」が左上、「ポケモン」がその右にあること
         * 6.オフライン状態であること
         * 7.無線のコントローラーが接続されていないこと
         */
        '''       
        print("---------------------------------------")
        print("自動リリース(剣盾)_v1.0")
        print("Copyright(c) 2024 tom dp")
        print("---------------------------------------")
        # 猶予時間告知
        print("このコマンドは1BOX内のポケモンを逃がす処理です")
        print("色違いは右隣のボックスへ移動させ、以外を逃がしますレポートを書き込みます")
        print("10秒後にコマンドを開始します")
        #10からカウントダウンさせる
        for i in range(10, -1, -1):
            #10から0までのカウントダウンを表示する
            print(str(i))
            self.wait(1)
        # repeat A ゲーム起動直後にコマンド実行してもいいようにする
        while not self.isContainTemplate("Network_Offline.png", threshold=0.9):
            self.press(Button.A, wait=3.0)
        self.wait(3)
        # メニューを開くよ
        self.press(Button.X, wait=0.6)
        self.press(Hat.TOP_LEFT, 1.0, wait=0.8)
        # ポケモン選択
        self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
        self.press(Button.A, wait=2)
        # ボックスを開く
        self.press(Button.R, wait=2)
        # ボックスを開くとデフォルトで左上にカーソルが入る
        # 色違いサーチ
        while True :
            is_contain_shiny = self.BoxSearchShiny()
            # メニューを閉じる
            self.press(Button.B, wait=0.5)
            self.press(Button.B, wait=2)
            self.press(Button.B, wait=2)
            self.press(Direction.LEFT, wait=0.5)  # set cursor to map
            self.press(Button.B, wait=1.5)
            # サーチ結果判定
            if is_contain_shiny:
                print('★★★shiny!★★★')
                # メニューを開くよ
                self.press(Button.X, wait=0.6)
                # ポケモン選択
                self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
                self.press(Button.A, wait=2)
                # ボックスを開く
                self.press(Button.R, wait=2)
                # ボックスを開くとデフォルトで左上にカーソルが入る
            else:
                break
        # メニューを開くよ
        self.press(Button.X, wait=0.6)
        # ポケモン選択
        self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
        self.press(Button.A, wait=2)
        # ボックスを開く
        self.press(Button.R, wait=2)
        # 逃がす処理
        self.ReleaseBox()
        # メニューを閉じる
        self.press(Button.B, wait=2)
        self.press(Button.B, wait=2)
        self.press(Direction.LEFT, wait=0.5)  # set cursor to map
        self.press(Button.B, wait=1.5)
        # 色違いがいればLINE通知
        if self.shiny_count > 0:
            self.LINE_image("[Eng]*** 色違い発見：" + str(self.shiny_count) + " ***")
        # レポートしておわり
        self.report()

    # デバッグ用メッセージ出力
    def debugMessage(self,methodName):
        #debug_message
        if self.debug:
            print("_method(AutoHatching_pkmnSWSH)_" + methodName)

    # 色違いサーチ
    def BoxSearchShiny(self):
        #debug_message
        self.debugMessage("BoxSearchShiny")
        row = 5
        col = 6
        #0～row-1までのrow回分
        for i in range(0, row):
            #0～col-1までのcol回分
            for j in range(0, col):

                # 色違いがいればボックス移動
                if self.isContainTemplate('shiny_mark.png', threshold=0.9):
                    self.moveBoxShiny()
                    return True

                # セル横移動
                if not j == col - 1:
                    if i % 2 == 0:
                        self.press(Direction.RIGHT, wait=0.2)
                    else:
                        self.press(Direction.LEFT, wait=0.2)
            # セル行移動
            self.press(Direction.DOWN, wait=0.2)
        return False

    # 色違いを隣のボックスに移動
    def moveBoxShiny(self):
        #debug_message
        self.debugMessage("moveBoxShiny")
        # メニュー表示
        self.press(Button.A, wait=0.5)
        # いどうする
        self.press(Button.A, wait=0.5)
        # てもちの一番下へ移動
        self.press(Hat.LEFT, duration=1.0, wait=0.5)
        self.press(Hat.BTM, duration=1.0, wait=0.5)
        # いちらんへカーソル移動
        self.press(Direction.RIGHT, wait=0.5)
        # いちらん表示
        self.press(Button.A, wait=0.5)
        # 右隣のボックスへ移動
        self.press(Direction.RIGHT, wait=0.5)
        # いどう
        self.press(Button.A, wait=0.5)
        # 元のボックスに戻る
        self.press(Direction.LEFT, wait=0.5)
        # 元のボックスを選択
        self.press(Button.A, wait=0.5)
        # 色違い数カウントアップ
        self.shiny_count += 1

    # BOXからリリース
    def ReleaseBox(self):
        #debug_message
        self.debugMessage("ReleaseBox")
        row = 5
        col = 6
        #0～row-1までのrow回分
        for i in range(0, row):
            #0～col-1までのcol回分
            for j in range(0, col):

                # Maybe this threshold works for only Japanese version.
                if self.isContainTemplate('status_Eng.png', threshold=0.7):
                    # Release a pokemon
                    self.Release()

                # セル横移動
                if not j == col - 1:
                    if i % 2 == 0:
                        self.press(Direction.RIGHT, wait=0.2)
                    else:
                        self.press(Direction.LEFT, wait=0.2)
            # セル行移動
            self.press(Direction.DOWN, wait=0.2)
        return False

    # リリース
    def Release(self):
        #debug_message
        self.debugMessage("Release")
        self.press(Button.A, wait=0.5)
        self.press(Direction.UP, wait=0.4)
        self.press(Direction.UP, wait=0.4)
        self.press(Button.A, wait=1)
        self.press(Direction.UP, wait=0.4)
        self.press(Button.A, wait=1.5)
        self.press(Button.A, wait=0.5)

    # レポート
    def report(self):
        """
        レポートを書く
        """
        #debug_message
        self.debugMessage("report")
        self.press(Button.X, wait=0.6)
        self.press(Button.R, wait=1)
        self.pressRep(Button.A, repeat=2, interval=0.5)
        self.wait(3)
        #self.pressRep(Button.B, repeat=5, interval=0.5)