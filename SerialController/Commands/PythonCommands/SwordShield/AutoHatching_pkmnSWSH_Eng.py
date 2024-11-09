import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from ..Common.util_Switch_Poke import util_Switch_Poke
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat

class AutoHatching_pkmnSWSH(util_Switch_Poke):
    NAME = '@【剣盾】自動タマゴ孵化(英語版)'
    '''
    --------------------------------------------------------------------------------------
     自動タマゴ孵化(SWSH)_v1.0 Release.2024/4/13
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
        # モード設定    1=色違いのみチェック 2=良個体もチェック 3=色違いが見つかったときのみ良個体もチェック
        self.mode = 1           
        # その他設定値
        self.shiny_max = 1                      # 色違い取得最大数を指定するための変数  色違い取得後にレポートを書かないようにしたい場合は1にします
        # 通知設定
        self.use_LINEnotice = True              # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになります True
        self.debug = False                       # debug用 True=デバッグようメッセージを出力
        self.debug_img_display = True           # debug用 True=エラー時の画像をLINEに送信（use_LINEnoticeがFalseだと、TrueにしてもFalseとして処理されます）
        self.debug_messege_display = False      # debug用 True=処理確認用のメッセージをログに出力
        # 個体値設定
        # [H,A,B,C,D,S]の順で、残しておきたい個体値を配列型で列挙する（0、31、99=任意） 
        self.status = [[31,31,31,31,31,31],[31,99,31,31,31,31],[31,31,31,31,31,99],[31,31,31,99,31,31]]    
        
        # カウンタ（編集不要）
        self.hatched_egg_total = 0  # タマゴ孵化数合計をカウントするための変数
        self.shiny_total = 0        # 色違い取得数をカウントするための変数
        
        # 歩く走る秒数   ★
        self.egg_sec = 20
        # 卵孵化した数
        self.egg_num_total = 0
        # 手持ちの卵が孵化した数
        self.egg_num = 0
        # ボックスに置くときの列位置
        self.box_line = 0
        # 色違い発見数
        self.shiny_count = 0
        # ループ回数
        self.roop_count = 0
        # 色違い発見フラグ  
        self.shiny_flag = False #1ループ内でのフラグ。次のループ処理に移ったらクリア

    def do(self):   
        '''
        /**
         * 育て屋から卵を回収→孵化→ボックスに預けるを繰り返すスケッチ
         * ボックスに空きがある限り、ポケモンを孵化し続ける
         *
         * 初期条件は以下の通り
         * 1.ハシノマはらっぱにいること
         * 2.自転車に乗っていること
         * 3.手持ちが1体のみのこと
         * 4.Xボタンを押したときに「タウンマップ」が左上、「ポケモン」がその右にあること
         * 5.ボックスが空のこと
         * 6.オフライン状態であること
         * 7.無線のコントローラーが接続されていないこと
         * 8.「設定」から「話の速さ」を「速い」に、「手持ち／ボックス」を「自動で送る」に、「ニックネーム登録」を「しない」にしておくこと
         */
        '''       
        print("---------------------------------------")
        print("自動タマゴ孵化(剣盾英語版)_v1.0")
        print("Copyright(c) 2024 tom dp")
        print("---------------------------------------")
        # 色違い最大数を入力させる
        #tkinter.Tk().withdraw()
        #self.shiny_max = tkinter.simpledialog.askinteger('色違い最大数入力', '色違い最大数を入力してください' ,initialvalue=1 , minvalue=1, maxvalue=30)
        print("▼" + str(self.shiny_max) + "匹の色違いを取得します▼")
        # 初期化処理
        if not self.use_LINEnotice:
            self.debug_img_display = False           # debug用 True=エラー時の画像をLINEに送信
        self.shiny_count = 0
        while True:
            # 時刻表示
            print(datetime.datetime.now())
            # repeat A ゲーム起動直後にコマンド実行してもいいようにする
            while not self.isContainTemplate("Network_Offline.png", threshold=0.9):
                self.press(Button.A, wait=3.0)
            # クリア
            self.box_line = 0
            self.shiny_flag = False
            # カウントアップ
            self.roop_count += 1
            # 起動時に1度だけ行われる処理 #
            self.setup()
            # 空を飛ぶ（位置情報リセット）
            self.moveToInitialPlayerPosition()
            # 走り回るぜ！！指定の秒数まで
            self.runAround(conditions=2,egg_sec=self.egg_sec)
            self.wait(1)
            # メニューを開くよ
            self.press(Button.X, wait=0.6)
            # 預け家から卵回収→孵化→ボックスに預けるを繰り返し
            while True :
                # ログ
                print("孵化数：" + str(self.egg_num_total) + "(ループ" + str(self.roop_count) + "回目）")
                # 初期化処理
                self.egg_num = 0
                # ボックスに置くときの列位置
                self.box_line += 1
                # 1BOX分置いたら抜けるよ
                if self.box_line > 6:
                    # ログ
                    print("1BOX分のポケモン預け終わりました。")
                    break
                # 手持ちがいっぱいになるまで回収→孵化を繰り返しボックスに預ける
                while True :
                    # 空を飛ぶ（位置情報リセット）
                    self.moveToInitialPlayerPosition()
                    # 育て屋さんから卵をもらう
                    self.getEggFromBreeder()
                    # メニューを開くよ
                    self.press(Button.X, wait=0.6)
                    # 空を飛ぶ（位置情報リセット）
                    self.moveToInitialPlayerPosition()
                    # 走り回るぜ！！孵化するまで
                    self.runAround(conditions=1)
                    # 画面が切り替わるまでAボタンを押す
                    while not self.isContainTemplate("Network_Offline.png", threshold=0.9):
                        self.press(Button.A, wait=1.5)
                    # 手持ちの卵が孵化した数
                    self.egg_num += 1
                    # 卵孵化した数
                    self.egg_num_total += 1
                    # 手持ちがいっぱいになったときの処理
                    if self.egg_num == 5:
                        # ボックスに預ける処理を呼び出す
                        self.sendHatchedPokemonToBox(self.box_line)
                        break
                    # 手持ちがいっぱいでない場合は、メニューを開いてからループに戻る
                    else:
                        # メニューを開くよ
                        self.press(Button.X, wait=0.6)
            # ポケモン選択
            self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
            self.press(Button.A, wait=2)
            # ボックスを開く
            self.press(Button.R, wait=2)
            # ボックスを開くとデフォルトで左上にカーソルが入る
            
            # 色違いサーチ、退避
            self.BoxSearchShiny()
            # メニューを閉じる
            self.press(Button.B, wait=0.5)
            self.press(Button.B, wait=2)
            self.press(Button.B, wait=2)
            self.press(Direction.LEFT, wait=0.5)  # set cursor to map
            self.press(Button.B, wait=1.5)
            #色違いがいた場合
            if self.shiny_flag:
                # メニューを開くよ
                self.press(Button.X, wait=0.6)
                # ポケモン選択
                self.press(Direction.RIGHT, wait=0.5)  # set cursor to party
                self.press(Button.A, wait=2)
                # ボックスを開く
                self.press(Button.R, wait=2)
                # リリース
                self.ReleaseBox()
                # メニューを閉じる
                self.press(Button.B, wait=2)
                self.press(Button.B, wait=2)
                self.press(Direction.LEFT, wait=0.5)  # set cursor to map
                self.press(Button.B, wait=1.5)
                #レポート
                self.report()
                print("report")
                print("色違い数：" + str(self.shiny_count) +  "/" + str(self.shiny_max))
                self.LINE_image("[Eng]*** 色違い発見：" + str(self.shiny_count) + "/" + str(self.shiny_max) + " ***") # LINE通知
                # 色違い取得最大数に達するまで続ける
                if self.shiny_count < self.shiny_max:
                    continue
                # 色違い最大数に達したら終わり
                print("▲" + str(self.shiny_max) + "匹の色違いを取得が終わりました▲")
                break
            # いなければリセットして時刻表示の所から再処理する（処理構成を変える必要あり）
            else:
                #リセットしてもう1回
                #self.softReboot()
                self.softRebootSwitch()


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
    
    # 初期位置からぐるぐる走り回る関数
    '''
        ※終了条件  1：卵孵化するまで
                    2：指定した秒数
    '''
    def runAround(self,conditions,egg_sec=0):
        #debug_message
        self.debugMessage("runAround(conditions=" + str(conditions) + ")")
        # 動き出し
        self.press(Direction.RIGHT, duration=1)
        self.hold([Direction.RIGHT, Direction.R_LEFT])
        # 終了条件：1
        if conditions == 1:
            while not self.isContainTemplate("egg_notice_Eng.png"):
                self.wait(1)
            self.holdEnd([Direction.RIGHT, Direction.R_LEFT])
            #print("test_1_success")
            return
        # 終了条件：2
        if conditions == 2:
            self.wait(egg_sec)
            self.holdEnd([Direction.RIGHT, Direction.R_LEFT])
            #print("test_2_success")
            return
        # 異常終了
        print("終了条件が不正です[" + str(conditions) + "]")
        self.finish()
    
    # 初期位置から育て屋さんに移動しタマゴを受け取る関数
    def getEggFromBreeder(self):
        #debug_message
        self.debugMessage("getEggFromBreeder")
        # 自転車から降りる
        self.wait(1.5)
        self.press(Button.PLUS, wait=0.6)
        #預かりやさん前に移動
        self.wait(1.5)
        self.press(Direction.DOWN, duration=0.05, wait=1)
        self.press(Direction.DOWN, duration=1.5)    #0.8
        self.press(Direction.LEFT, duration=0.2, wait=0.5)
        # 自転車に乗る
        self.press(Button.PLUS, wait=1.0)
        # 育て屋さんに話しかける
        self.press(Button.A, wait=1.0)
        # 卵が孵化されていなかったときは初期位置に戻り、またグルグルする
        while not self.isContainTemplate("egg_found_Eng.png"):
            self.wait(1.0)
            self.pressRep(Button.B, repeat=10, interval=0.3)
            # メニューを開くよ
            self.press(Button.X, wait=0.6)
            # 空を飛ぶ（位置情報リセット）
            self.moveToInitialPlayerPosition()
            # 走り回るぜ！！指定の秒数まで
            self.runAround(conditions=2,egg_sec=self.egg_sec)
            self.wait(1)
            # メニューを開くよ
            self.press(Button.X, wait=0.6)
            # 空を飛ぶ（位置情報リセット）
            self.moveToInitialPlayerPosition()
            # 自転車から降りる
            self.wait(1.5)
            self.press(Button.PLUS, wait=0.6)
            # 預かりやさん前に移動
            self.wait(1.5)
            self.press(Direction.DOWN, duration=0.05, wait=1)
            self.press(Direction.DOWN, duration=1.5)    #0.8
            self.press(Direction.LEFT, duration=0.2, wait=0.5)
            # 自転車に乗る
            self.press(Button.PLUS, wait=1.0)
            # 育て屋さんに話しかける
            self.press(Button.A, wait=1.0)
        # 卵発見後、育て屋さんから卵をもらう
        self.pressRep(Button.A, repeat=2, interval=1.0)
        self.wait(4.0)
        self.pressRep(Button.B, repeat=10, interval=0.3)
        self.wait(2.5)

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
        
        ## ボックスがいっぱいになったら、次のボックスに移動させる
        #if (box_line == 5) {
        #    pushHat(Hat::UP, 25);
        #    pushHat(Hat::RIGHT, 25);
        #}
        
        # ボックスを閉じる
        self.press(Button.B, wait=0.5)  # ボックスが空でなかった場合でも、ボックスを閉じてループを実行し続けさせるのに必要な記述
        self.press(Button.B, wait=1.5)
        self.press(Button.B, wait=1.3)
        
        # メニュー画面のカーソルをタウンマップに戻す
        self.press(Hat.LEFT, duration=0.1 , wait=0.5)

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
                if self.isContainTemplate('shiny_mark_Eng.png', threshold=0.9):
                    shiny_row = i
                    # 偶数行目は右から探索するので補正が必要
                    if i % 2 == 0:
                        shiny_col = j
                    else:
                        shiny_col = col - j - 1
                    self.LINE_image("[Eng]★★★shiny!（" + str(self.egg_num_total) + "匹目）★★★")   # LINE通知
                    self.moveBoxShiny(shiny_row,shiny_col)
                    # 色違い発見フラグ
                    self.shiny_flag = True
                    # 色違い数カウントアップ
                    self.shiny_count += 1
                    print("★★★shiny!★★★")
                    #return True

                # セル横移動
                if not j == col - 1:
                    if i % 2 == 0:
                        self.press(Direction.RIGHT, wait=0.2)
                    else:
                        self.press(Direction.LEFT, wait=0.2)
            # セル行移動
            self.press(Direction.DOWN, wait=0.2)
        #return False

    # 色違いを隣のボックスに移動し、元の位置に戻る
    def moveBoxShiny(self,row,col):
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
        # 一度ボックスを閉じる
        self.press(Button.B, wait=2.5)
        # 再度ボックスを開ける
        self.press(Button.R, wait=2.5)
        print(str(row + 1) + "【行目】" + str(col + 1) + "【列目】へ移動")
        # ボックス内の初期位置から元の場所に移動(行)
        self.pressRep(Hat.BTM, repeat=row, interval=0.5, wait=0.5)
        # ボックス内の初期位置から元の場所に移動(列)
        self.pressRep(Hat.RIGHT, repeat=col, interval=0.5, wait=0.5)
        
        #print("▼色違い移動後、元の場所に復帰▼")

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

    # ソフト再起動
    def softReboot(self):
        #debug_message
        self.debugMessage("softReboot")
        # reset
        self.press(Button.HOME, wait=2)
        self.press(Button.X)
        self.press(Button.A, wait=4.5)
        # TOM_COMMENT 待ち時間増加(遅延対策) bak:1.5
        self.press(Button.A, wait=5)
        # TOM_COMMENT 待ち時間増加(サブ垢はソフトを遊べるかチェックがはいるのですこし待つ) bak:5
        self.press(Button.A, wait=10)
        return True

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
