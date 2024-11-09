import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from ..Common.util_Switch_Poke import util_Switch_Poke
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat

class AutoHatching_pkmnBDSP(util_Switch_Poke):
    NAME = '@【BDSP】自動タマゴ孵化'
    '''
    --------------------------------------------------------------------------------------
     自動タマゴ孵化(BDSP)_v1.0 Release.2024/9/8
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
        self.shiny_max = 2                      # 色違い取得最大数を指定するための変数  色違い取得後にレポートを書かないようにしたい場合は1にします
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
        
        # 歩く走る秒数
        self.egg_sec = 300  #★とりあえず仮置き
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

    # press button at duration times(s)
    def stick(self, buttons, duration=0.1, wait=0.1):
        self.keys.input(buttons, ifPrint=False)
        # print(buttons)
        self.wait(duration)
        self.wait(wait)
        self.checkIfAlive()

    # press button at duration times(s)
    def stickEnd(self, buttons):
        self.keys.inputEnd(buttons)
        self.checkIfAlive()

    def do(self): 
        '''
        * 育て屋から卵を回収→孵化→ボックスに預けるを繰り返すスケッチ
        * ボックスに空きがある限り、ポケモンを孵化し続ける
        *
        * 初期条件は以下の通り
        * 1.ズイタウンにいること
        * 2.ショートカットに自転車のみが登録された状態であること（＋ボタンで自転車に乗れること）
        * 3.自転車を4速にしておくこと
        * 4.手持ちが「ほのおのからだ」の特性持ちの1体のみのこと
        * 5.「まるいおまもり」を所持していること
        * 6.Xボタンを押したときに「タウンマップ」が左上、「ポケモン」がその右にあること
        * 7.空のボックスが続いた状態であること
        * 8.無線のコントローラーが接続されていないこと
        * 9.「設定」から「話の速さ」を「速い」に、「手持ち／ボックス」を「自動で送る」に、「ニックネーム登録」を「しない」にしておくこと
        * 10. ズイタウン周辺のトレーナーを全員倒しておくこと
        '''
        '''
            前提：手持ちの先頭はほのおのからだなどのとくせい持ちにしておく
            　　　２～６匹目は何でもいいので埋めておく
            　　　卵を預ける空のＢＯＸの直前のBOXの最右列５匹分は空けておく
            　　　ショートカットは自転車のみにしておく
            　　　空のＢＯＸの最初の位置を初期位置にしておく
            処理内容：
            １．初期処理を行う
            以下Ｘを条件を満たすまでループする
            Ｘ：無条件
                Ｘ１．時刻表示
                Ｘ２．コマンド開始できるまで繰り返し処理をさせる　※画像：ポケッチの画像
                Ｘ３．クリア　box_line　shiny_flag、カウントアップ処理　roop_count
                Ｘ４．起動時処理を行う
                以下Ａを条件を満たすまでループする
                Ａ：タマゴを指定数受け取るまで
                    Ａ１．初期位置に戻る
                    Ａ２．走り回る（タマゴが産まれる秒数）Lay an egg
                    Ａ３．初期位置に戻る
                    Ａ４．育てやに話しかける。たまごが無ければ１．に戻る　※画像：メッセージボックス
                    Ａ５．タマゴをもらう
                Ｘ５．メニューを開く
                Ｘ６．ＢＯＸを開く
                　　範囲選択に切り替える
                Ｘ７．タマゴＢＯＸの左隣のＢＯＸに移動
                Ｘ８．手持ちの２～６匹目をＢＯＸに預ける（掴んだらいちらんからＢＯＸへドロップ）
                Ｘ９．タマゴＢＯＸに移動
                （いったんメニューを閉じて再度タマゴＢＯＸを開く）←いらんやろ
                以下Ｂを条件を満たすまでループする
                Ｂ：１ＢＯＸ分タマゴが孵化するまで
                    Ｂ１．タマゴＢＯＸから列単位でタマゴ取り出す
                    Ｂ２．この時に卵の数をカウントする　currentEggs
                    　　Ｂボタンでメニュー閉じる
                    Ｂ３．Ａボタンを押下し続ける
                    以下Ｂを条件を満たすまでループする
                    Ｃ：おや表示回数　≧　currentEggs
                        Ｃ１．初期位置に戻る
                        Ｃ２．走り回る（孵化秒数）eggs hatch
                        Ｃ３．おや。。。？のメッセージ表示回数をカウント　※画像：おや。。。のメッセージＢＯＸ
                    Ｂ４．１０秒待つ
                    Ｂ５．Ａボタンを押下辞める
                    Ｂ６．メニューを開く
                    Ｂ７．ＢＯＸを開く
                    Ｂ８．手持ちの２～６匹目の色違い判定を行いカウントする shiny_flag　※画像：色違いＭａｒｋ
                    Ｂ９．範囲選択に切り替える
                    Ｂ１０．手持ちの２～６匹目を範囲選択する
                    Ｂ１１．孵化したポケモンをタマゴＢＯＸにあずける
                Ｘ９．メニューを閉じる
                以下Ｄを条件を満たす場合の処理を行う
                Ｄ：shiny_flag = True
                    Ｄ１．メニューを開く
                    Ｄ２．ＢＯＸを開く
                    以下Ｅを条件を満たすまでループする
                    Ｅ：ＢＯＸ内のすべてのポケモンを探索するまで
                        Ｅ１．色違いポケモンを探索する　※画像：ボックスの名前画像、背景注意
                        　　　この時、行列で何マス移動したのかカウントしておく　row_count　row_count
                        以下Ｆを条件を満たす場合の処理を行う
                        Ｆ：色違い発見
                            Ｆ１．色違いを発見したらカウントする　shiny_count　
                            　　　指定のＢＯＸに移動させる。移動する際に移動したＢＯＸ数をカウントする　move_box_count
                            Ｆ２．move_box_countの分だけＢＯＸ移動し、元のＢＯＸに場所を戻す
                            Ｆ３．row_count　row_countの分だけマス移動し、元のマス位置に場所を戻す
                            （Ｆ１でいちらんから色違いをドロップさせておけば不要かも。→自動で元の位置に戻るかもしれない要検証）
                    Ｄ３．メニューを閉じる
                以下Ｇを条件を満たす場合の処理を行う
                Ｇ：shiny_count ≧ shiny_total
                    Ｇ１：Ｘを終了する
                Ｘ１０．再起動処理を行う



            

        '''
        print("---------------------------------------")
        print("自動タマゴ孵化(BDSP)_v1.0")
        print("Copyright(c) 2024 tom dp")
        print("---------------------------------------")
        # 初期化処理
        if not self.use_LINEnotice:
            self.debug_img_display = False           # debug用 True=エラー時の画像をLINEに送信
        self.shiny_count = 0
        while True:
            # 時刻表示
            print(datetime.datetime.now())
            # ★画像を差し替える
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
            # 「そらをとぶ」を使うことで、位置情報をリセットする
            self.moveToInitialPlayerPosition()
            # 初めのタマゴが出現するまで走り回る
            #tiltLeftStick(Stick::MIN, Stick::NEUTRAL, 560);
            #pushButton(Button::PLUS, 600);
            #tiltLeftStick(Stick::NEUTRAL, Stick::MIN, 5900);
            #tiltLeftStick(Stick::NEUTRAL, Stick::MAX, 10400);
            #tiltLeftStick(Stick::NEUTRAL, Stick::MIN, 10400);
            #tiltLeftStick(Stick::NEUTRAL, Stick::MAX, 4800);
            self.runAround(self.egg_sec);
            # 「そらをとぶ」を使う前に、ズイタウンにいることを確定させる
            self.press(Hat.BTM, duration=1.0, wait=0.5)     # 下に走る
            # メニューを開く
            self.press(Button.X, wait=0.75)
            # メニューの左上にカーソルを持っていく
            self.press(Hat.TOP_LEFT, 1.5, wait=0.8)
            # ここに記述した内容がループされ続ける
            for box_line in range(0, 6):
                self.receiveAndHatchEggs(box_line)

    # デバッグ用メッセージ出力
    def debugMessage(self,methodName):
        #debug_message
        if self.debug:
            print("_method(AutoHatching_pkmnBDSP)_" + methodName)

    # 起動時に1度だけ行われる処理
    def setup(self):
        #debug_message
        self.debugMessage("setup")
        # Switchがマイコンを認識するまでは信号を受け付けないため、適当な処理をさせておく
        self.pressRep(Button.L, 5, interval=0.5)
        # print("マイコン認識動作終了")
        # メニューの左上にカーソルを持っていく
        self.press(Button.X, wait=0.75)
        self.press(Hat.TOP_LEFT, 1.5, wait=0.8)

    # 空飛ぶでズイタウンに移動する関数
    def moveToInitialPlayerPosition(self):
        #debug_message
        self.debugMessage("moveToInitialPlayerPosition")
        #pushButton(Button::A, 2000);
        #pushButton(Button::A, 1000, 2);
        #delay(7000);
        self.press(Button.A, wait=2.0)
        self.pressRep(Button.A, 2, interval=1.0)
        self.wait(7.0)
    
    # ★これだと受け取れないので修正が必要
    # 初期位置から育て屋さんに移動しタマゴを受け取る関数    
    def getEggFromBreeder(self):
        #debug_message
        self.debugMessage("getEggFromBreeder")
        # 初期位置(ズイタウンのポケモンセンター)から育て屋さんのところまで移動
        self.press(Hat.LEFT, duration=1.3, wait=0.5)    # 左に歩く
        self.press(Hat.TOP, duration=0.1, wait=0.5)     # 上を向く
        self.pressRep(Hat.TOP, repeat=9, interval=0.3)  # 上に歩く
        self.press(Hat.LEFT, duration=1.5, wait=0.5)    # 左に歩く
        # 育て屋さんから卵をもらう
        self.press(Button.A, wait=0.5)                  # Aボタン   預け家に話しかける
        self.pressRep(Button.B, 1, interval=0.5)        # Bボタンを2回押す  ★
        self.pressRep(Button.A, 2, interval=0.5)        # Aボタンを2回押す
        self.pressRep(Button.B, 2, interval=0.5)        # Bボタンを2回押す
        self.press(Button.A, wait=0.5)                  # Aボタン
        self.pressRep(Button.B, 10, interval=0.5)        # Bボタンを10回押す
        
    # 初期位置(ズイタウンのポケモンセンター)からタマゴが孵化するまで走り回る関数
    def runAround(self, egg_sec=0):
        #debug_message
        self.debugMessage("runAround")
        self.press(Hat.LEFT, duration=1.45, wait=0.5)    # 左に歩く
        self.press(Button.PLUS)                         # 自転車に乗る
        self.press(Hat.TOP, duration=2.0, wait=0.5)     # 上に走る

        angle = 0
        i = 0
        self.cnt =0
        r = 0.5
        while not self.cnt > egg_sec:
            '''
            ここには動作サンプルコードを書く。スティック補正画面で挙動確認ができる。
            全体を通して極座標で考えていく。（角度と大きさで曲線をあらわす)
            
            なお、通常はself.press()を使うが、連続的にスティックを動かすとログが多すぎるので、self.stick()関数を作って使っている。
            
            angle : 角度(Degree)
            r :　スティックの傾き度合い(0<=r<=1.0)、1.0で傾き最大
            
            以下はr=0.5でangleを増加させながらstickを動かすコード
            50%位置をスティックが円形に移動する
            stickEnd()を行わないとスティックが入力されっぱなしになるので注意
            '''

            #r = 0.5
            self.stick(Direction(Stick.LEFT, angle, r, showName=f'Angle={angle},r={r}'), duration=0.0, wait=0.0)
            angle += 5
            i += 1
            self.cnt += 1
            # ★画像認識で卵が産まれたかを認識し孵化したらループ終了とする
        self.stickEnd(Direction(Stick.LEFT, i, i / 360, showName=f'Angle={angle},r={r}'))

    # タマゴが孵化するのを待つ関数
    def waitEggHatching(self):
        #debug_message
        self.debugMessage("waitEggHatching")
        self.pressRep(Button.A, 30, interval=0.5)        # Aボタンを30回押す
        self.wait(4.0)

    # 孵化した手持ちのポケモンをボックスに預ける関数
    # box_line : 何列目にポケモンを預けるか
    def sendHatchedPokemonToBox(self, box_line):
        #debug_message
        self.debugMessage("sendHatchedPokemonToBox")
        # ボックスを開く
        self.press(Button.X, wait=0.5)
        self.press(Hat.RIGHT, wait=0.05)
        self.press(Button.A, wait=1.25)
        self.press(Button.R, wait=1.5)
        # 手持ちの孵化したポケモンを範囲選択
        self.press(Hat.LEFT, wait=0.05)
        self.press(Hat.BTM, wait=0.05)
        self.pressRep(Button.Y, 2, interval=0.05)
        self.press(Button.A, wait=0.05)
        self.press(Direction.DOWN, duration=1.2)
        self.press(Button.A, wait=0.05)
        # ボックスに移動させる
        self.pressRep(Hat.RIGHT, box_line + 1, interval=0.1)
        self.press(Hat.TOP, wait=0.05)
        self.press(Button.A, wait=0.05)
        # ボックスがいっぱいになったら、次のボックスに移動させる
        if box_line == 5:
            self.press(Hat.TOP, wait=0.05)
            self.press(Hat.RIGHT, wait=0.5)
        # ボックスを閉じる
            self.press(Button.B, wait=0.05) # ボックスが空でなかった場合でも、ボックスを閉じてループを実行し続けさせるのに必要な記述
            self.press(Button.B, wait=1.5)
            self.press(Button.B, wait=1.25)
        # メニュー画面のカーソルをタウンマップに戻す
        self.press(Hat.LEFT, wait=0.5)

    # 実際にループ内で呼び出す関数
    def receiveAndHatchEggs(self, box_line):
        #debug_message
        self.debugMessage("receiveAndHatchEggs")
        # 手持ちが1体の状態から、卵受け取り→孵化を繰り返していく
        for egg_num in range(0, 5):
            self.moveToInitialPlayerPosition()
            self.getEggFromBreeder()
            self.press(Button.X, wait=0.5)
            self.moveToInitialPlayerPosition()
            self.runAround(self.egg_sec)
            self.waitEggHatching()
            # 「そらをとぶ」を使う前に、ズイタウンにいることを確定させる
            self.press(Hat.BTM, duration=1.0, wait=0.5)     # 下に走る
            # 手持ちがいっぱいになったときの処理
            if egg_num == 4:
                # ボックスに預ける処理を呼び出す
                self.sendHatchedPokemonToBox(box_line);
            else:
                # 手持ちがいっぱいでない場合は、メニューを開いてからループに戻る
                self.press(Button.X, wait=0.5)