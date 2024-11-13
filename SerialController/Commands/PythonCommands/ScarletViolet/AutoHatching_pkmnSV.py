import time
import datetime

from .SV_util_box import SV_util_box
from .SV_util_picnic import SV_util_picnic
from ..Common.util_Switch_Poke import util_Switch_Poke
from Commands.Keys import Button, Direction,Stick

class AutoHatching_pkmnSV(SV_util_box,SV_util_picnic,util_Switch_Poke):
    NAME = '@【ＳＶ】自動タマゴ孵化(SV)'
    '''
    --------------------------------------------------------------------------------------
     自動タマゴ孵化(SV)_v3.5 Release.2023/1/18
     Copyright(c) 2023 mikan kato
     ◆改修内容
        ・doメソッド内色違いのカウント数バグを修正
        ・コメントの日本語化
    --------------------------------------------------------------------------------------
    '''
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
        self.egg_max = 30                       # ピクニックタマゴ取得数を指定するための変数
        self.shiny_max = 3                      # 色違い取得最大数を指定するための変数  色違い取得後にレポートを書かないようにしたい場合は1にします
        # 通知設定
        self.use_LINEnotice = True              # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになります True
        self.debug_img_display = True           # debug用 True=エラー時の画像をLINEに送信（use_LINEnoticeがFalseだと、TrueにしてもFalseとして処理されます）
        self.debug_messege_display = False      # debug用 True=処理確認用のメッセージをログに出力
        # 個体値設定
        # [H,A,B,C,D,S]の順で、残しておきたい個体値を配列型で列挙する（0、31、99=任意） 
        self.status = [[31,31,31,31,31,31],[31,99,31,31,31,31],[31,31,31,31,31,99],[31,31,31,99,31,31]]    
        
        # カウンタ（編集不要）
        self.hatched_egg_total = 0  # タマゴ孵化数合計をカウントするための変数
        self.shiny_total = 0        # 色違い取得数をカウントするための変数
        # 共通フラグ（編集不要）
        self.IV_flag = False    
        #TOM_COMMENT 特定ポケモン用のフラグを追加
        #FIXME 成功したらEng版の方にも反映
        self.tokupokeflag = True                # おそらくだが、メテノ（紫）やコオリッポなど特定ポケモンは手持ちにいるとタマゴ判定されやすいので、判定条件に閾値を設けるかのフラグを設定する

    def do(self):   
        '''
        ◆◆◆概要◆◆◆
        ※手持ちにタマゴがない場合
        <0-1>「きじゅん」ボックスにいるポケモン（親）を手持ちに入れる
        <0-2>キャンプを開いて料理・30個タマゴを取得
        <0-3>「たまご」ボックスからタマゴを手持ちに移動
        ※以降共通
        <1>手持ちにあるタマゴをすべて孵化
        <2>「たまご」ボックスに孵化ポケモンを移動、色違いの場合は右隣のボックスに移動
            色違いがいれば色違いありフラグを立てる
        <3>「たまご」ボックスからタマゴを手持ちに移動
        <4>「たまご」ボックスからタマゴがなくなったらボックス内のチェックを実施
            色違いありフラグが立って入れば逃がす処理を実行
        <5> 色違い取得数が上限に達していれば処理を終了
        <6> 色違いがいればレポートを書く
        <7> リセット
        ◆◆◆事前設定◆◆◆
        ニックネーム設定    <OFF>
        オートセーブ        <OFF>
        スタート位置        <ゼロゲート>
        ボックス表示        <ジャッジ>
        サンドイッチ材料    <スーパーピーナッツバターサンド>複数個分
        スタート時手持ち    孵化要員1匹のみ（特性ほのおのからだ等）
        ボックス配置：      [きじゅん][たまご][任意]の順で横並びにする
            「きじゅん」ボックス
                ・親ポケモンを置くボックス
                ・背景はデフォルトのもの
                ・ボックス左端列の1列目1行目と2列目（複数匹可）に親ポケモンを配置
            「たまご」ボックス
                ・タマゴを置くボックスなのでポケモンを置かないこと
                ・背景はデフォルトのもの
                ・「きじゅん」ボックスの右横に配置する
            良個体・色違いを置くボックス
                ・色違い、良個体を見つけた時に移動するためのボックス
                ・背景はデフォルトのもの
                ・「たまご」ボックスの右横に配置する
        ※開始時は、たまごボックスが開く状態でボックスを閉じておくとよい
        ※タマゴ取得後から開始する場合
            手持ちを孵化要員1匹（特性ほのおのからだ等）+タマゴにするとタマゴ取得処理をスキップできる。
            ボックスを開いたときにタマゴがある状態にしたうえで、
            孵化したいタマゴをボックス内の左上から詰めておいておくとそのボックス内のタマゴを自動で孵化する。
        '''       
        print("---------------------------------------")
        print("自動タマゴ孵化(SV)_v3.5")
        print("Copyright(c) 2023 mikan kato")
        print("---------------------------------------")
        ############################################
        import tkinter as tk

        def get_entry():
            self.shiny_max = int(entry.get())
            root.destroy()

        root = tk.Tk()
        root.title('Entry')
        root.geometry( '300x300' + '+1280+540' )

        entry = tk.Entry(root, width=20)
        # 初期値を入れておく
        entry.insert(0, self.shiny_max)
        entry.pack(pady=10)

        button = tk.Button(root, text='反映', command=get_entry)
        button.pack()

        root.mainloop()
        ############################################
        print("▼" + str(self.shiny_max) + "匹の色違いを取得します▼")
        if not self.use_LINEnotice:
            self.debug_img_display = False           # debug用 True=エラー時の画像をLINEに送信
        # 以下繰り返し
        while True :    
            # 時刻表示
            print(datetime.datetime.now())
            # repeat A ゲーム起動直後にコマンド実行してもいいようにする
            while not self.isContainTemplatePositionBGR(
                "SV_util\_player_marker.png",
                threshold=0.7,
                mask_path="SV_util\_mask_playermarker.png",
                lower=[0, 200, 200],
                upper=[8585, 255, 255],
            ):
                self.press(Button.A, wait=3.0)
            # 初期化
            self.IV_flag = False    
            shiny_putHatchedEggs = 0
            shiny_checkBox= 0    
            # 手持ちのタマゴ数を確認するタマゴ取得処理を行うか判断する
            eggs = self.checkPartyEggs()
            # ========================================================================
            # <0>タマゴがない場合、タマゴ取得処理を行う
            if eggs == 0 :
                # プレイヤーの位置を初期化する
                if not self.resetPositionZerogate():          
                    # 上手くいかなかった場合はソフト再起動
                    # self.softReboot()
                    self.softRebootSwitch()
                    continue
                # <0-1>手持ちを変更する（孵化要員->親要員）
                if not self.changePokemonToParent():          
                    # 上手くいかなかった場合はソフト再起動
                    # self.softReboot()
                    self.softRebootSwitch()
                    continue
                # <0-2>ピクニックを開いてタマゴをegg_max個取得する
                # なぜか指定数ぴったりにならない場合があるが、支障がないので原因究明は未実施
                if not self.getNewEgg(self.egg_max) :    
                    # 上手くいかなかった場合はソフト再起動
                    # self.softReboot()
                    self.softRebootSwitch()
                    continue
                # 手持ちを変更する（親要員->孵化要員）
                if not self.changePokemonToHatching():    
                    # 上手くいかなかった場合はソフト再起動
                    # self.softReboot()
                    self.softRebootSwitch()
                    continue
                # <0-3>タマゴを手持ちに入れ、手持ちのタマゴ数を確認する
                eggs = self.pullEggs()
            # ========================================================================
            # 手持ちタマゴの孵化処理を行う
            while True:
                # プレイヤーの位置を初期化する
                if not self.resetPositionZerogate():       
                    # 上手くいかなかった場合はソフト再起動
                    # self.softReboot()
                    self.softRebootSwitch()
                    continue 
                # <1>手持ちタマゴの数分、孵化を行う
                self.hatching(eggs) 
                # <2>孵化したポケモンをボックスに戻す
                # 色違いがいた場合数をカウントし、後続処理でボックスの逃がし処理を行う
                shiny_putHatchedEggs += self.putHatchedEggs()   
                # <3>タマゴを手持ちに入れ、手持ちのタマゴ数を確認する
                eggs = self.pullEggs()
                if eggs == 0:
                    # タマゴがなければボックス内全てのタマゴ孵化が終了したため孵化処理を終了する
                    break  
            # ========================================================================
            # putHatchedEggsで色違い/指定個体値を見落とした場合を考慮して、念のためボックス全体の色違いチェックをする
            if shiny_putHatchedEggs <= 0 and not self.IV_flag:
                if self.mode == 2 :
                    # 色違い/ステータスを確認する
                    shiny_checkBox = self.checkBox(statuscheck_flag=True)    
                else:
                    # 色違いを確認する
                    shiny_checkBox = self.checkBox()
                # ここまでで色違いがいた場合合計に加算する
                self.shiny_total += shiny_checkBox 
            # ========================================================================
            # <4>色違い/指定個体値がいた場合、ボックスの逃がし処理をする
            if shiny_putHatchedEggs > 0 or shiny_checkBox > 0 or self.IV_flag:
                # 色違い数が指定数以下の場合逃がす処理を行う
                # putHatchedEggsで見つけた色違い/指定個体値は移動していないので、ここで移動を行う
                if self.shiny_total < self.shiny_max:      
                    if self.mode == 1 :
                        # 色違いを確認する
                        print('release box (mode:1)')   
                        self.shiny_total += self.checkBox(release_flag=True)
                    else:
                        # 色違い/ステータスを確認する
                        print('release box (mode:2,3)')   
                        self.shiny_total += self.checkBox(release_flag=True,statuscheck_flag=True)
                # 色違い数が指定数以上であれば終了
                if self.shiny_total >= self.shiny_max: 
                    print('PGM end')                        
                    self.finish()
                # <6>レポートを書く
                print('report') 
                # LINE送信   
                # if self.use_LINEnotice:
                    # self.LINE_image('report')    # LINE通知不要なら削除 
                    # self.LINE_image("*** 色違い発見：" + str(self.shiny_total) + "/" + str(self.shiny_max) + " ***") # LINE通知
                self.report()
            # <7>リセットする
            else:
                #self.softReboot()
                self.softRebootSwitch()

    def checkPartyEggs(self):
        """
        手持ちのタマゴ数を確認する
        【戻り値】int タマゴ数
        """
        # x menu
        self.openXmenu()
        # eggs
        eggs = self.countEggsInParty()
        # x close
        self.press(Button.B, wait=3)
        return eggs

    def countEggsInParty(self):
        """
        手持ちのタマゴ数を確認する
        【戻り値】int タマゴ数
        """
        eggs = 0
        if self.isContainTemplate('SV_AutoHatching\menu_eggs1.png',threshold=0.9): 
            eggs=1
            if self.isContainTemplate('SV_AutoHatching\menu_eggs5.png',threshold=0.9):   
                eggs=5        
            elif self.isContainTemplate('SV_AutoHatching\menu_eggs4.png',threshold=0.9):   
                eggs=4
            elif self.isContainTemplate('SV_AutoHatching\menu_eggs3.png',threshold=0.9):   
                eggs=3
            elif self.isContainTemplate('SV_AutoHatching\menu_eggs2.png',threshold=0.9):   
                eggs=2
        print('eggs: ',eggs)
        return eggs

    def resetPositionZerogate(self):
        """
        そらをとんでゼロゲート前に移動
        【戻り値】bool 成否
        """
        # initialize
        map_zerogate = 'SV_AutoHatching\Ymenu_map_zerogate.png'
        # 空を飛ぶ
        if not self.resetPosition(target_path=map_zerogate):
            return False
        # walk
        self.press(Direction(Stick.LEFT, 60), duration=3.5, wait=0.5) 
        return True
         

    def getNewEgg(self,egg=30):
        """
        ピクニックを開いてタマゴを取得する（サンドイッチを作る）
        【前提】ピクニックを開いた状態
        【戻り値】bool 成否

        Parameters
        ----------
        egg : int
            取得したいタマゴ数を設定すると、その数分バスケットからタマゴを取得する
        """
        print('_method_getNewEgg')
        # initialize
        recipe_path='SV_AutoHatching\sandwich.png'          # 作りたいサンドイッチの画像パス
        power_path='SV_AutoHatching\sandwich_power_lv2.png' # 発動させたいパワーレベルの画像パス
        repeatcount_max=17                                  # サンドイッチレシピを選択する時の、最大右ボタン押下数（入力失敗時にやり直す）
        # open
        self.openPicnic()
        # walk to table
        self.press(Direction.DOWN, duration=0.3)
        # cook start
        if not self.makeSandwich(recipe_path=recipe_path,power_path=power_path,repeatcount_max=repeatcount_max):
            return False                                    # 指定したパワーが発動しなかったときはFalseを返す
        # walk to basket      
        self.press(Button.B) 
        self.press(Direction.RIGHT, duration=0.5, wait=0.5) 
        self.press(Direction.DOWN, duration=1, wait=0.5)
        self.press(Direction.LEFT, duration=0.1, wait=0.5)
        # check basket
        if not self.checkBasket(egg) :
            return False    
        # close
        self.closePicnic()          
        return True


    def changePokemonToParent(self):
        '''
        手持ちを親ポケモンに変更し、隣のタマゴ用ボックスを表示して終了する
        【前提】BOXを開いた状態から実行、"きじゅん"box内に親ポケモンを配置しておく
        【戻り値】bool 成否
        '''  
        print('_method_changePokemonToParent')
        # open
        self.openBox()
        # move box
        self.moveBox('SV_AutoHatching\inbox_title_base.png')  
        # focus move to party          
        self.moveCellFocus(row=1,column=0)
        # put Hatcher
        self.press(Button.Y, wait=0.3)  # pull
        self.moveCellFocus(row=1,column=1)        
        self.press(Button.Y, wait=0.3)  # put
        self.moveCellFocus(row=1,column=2)
        self.press(Button.MINUS, wait=0.3)
        self.press(Direction.DOWN, duration=0.6, wait=0.3)
        self.press(Button.A, wait=0.5)
        self.moveCellFocus(row=2,column=0)
        self.press(Button.A, wait=0.5)
        # next box
        self.press(Button.R, wait=0.3)
        self.moveBox('SV_AutoHatching\inbox_title_egg.png')                 # 念のためボックス名を確認
        # check party
        if self.isContainTemplate('SV_AutoHatching\inbox_party_null_5.png',area=[0,720,0,300]):
            print('ERROR : changePokemonToParent - connot moved pkmn')
            # send LINE
            if self.debug_img_display:
                self.LINE_image('ERROR : changePokemonToParent - connot moved pkmn')    # デバッグ用  
            return False    
        # close
        self.closeBox()     
        return True


    def changePokemonToHatching(self):
        '''
        手持ちをタマゴ孵化用ポケモンに変更し、隣のタマゴ用ボックスを表示して終了する
        【前提】BOXを開いた状態から実行、"きじゅん"box内に孵化用ポケモンを配置しておく
        【戻り値】bool 成否
        '''
        print('_method_changePokemonToHatching')
        # open
        self.openBox()
        # move box
        self.moveBox('SV_AutoHatching\inbox_title_base.png')  
        # focus move to lefttop
        self.moveCellFocus(row=1,column=1)
        # put parent
        self.press(Button.Y, wait=0.3)  # pull
        self.moveCellFocus(row=1,column=0)        
        self.press(Button.Y, wait=0.3)  # put
        self.moveCellFocus(row=2,column=0)
        self.press(Button.MINUS, wait=0.3)
        self.press(Direction.DOWN, duration=0.6, wait=0.3)
        self.press(Button.A, wait=0.5)
        self.moveCellFocus(row=1,column=2)
        self.press(Button.A, wait=0.5)
        # next box
        self.press(Button.R, wait=0.3)
        self.moveBox('SV_AutoHatching\inbox_title_egg.png')                 # 念のためボックス名を確認
        # check party
        if not self.isContainTemplate('SV_AutoHatching\inbox_party_null_5.png',area=[0,720,0,300]):   
            print('ERROR : changePokemonToHatching - connot moved pkmn')
            # send LINE
            if self.debug_img_display:
                self.LINE_image('ERROR :changePokemonToHatching - connot moved pkmn')    # デバッグ用
            return False
        return True

            
    def hatching(self,eggs=5):
        """
        タマゴ孵化処理
        【戻り値】bool 成否

        Parameters
        ----------
        eggs : int
            手持ちのタマゴの数を引数に設定すると、その数分孵化処理を行う
        """        
        print('_method_hatching')
        # Ride TOM_COMMENT 遅延対策 bak:0.5
        self.press(Button.PLUS, wait=2.5)  
        for i in range(0, eggs):
            count = 0
            # start run
            self.hold([Direction(Stick.LEFT, 85), Direction(Stick.RIGHT, 180)])
            self.press(Button.LCLICK)  
            # hatching notice
            while not self.isContainTemplate('SV_AutoHatching\message_hatching.png'):
                self.press(Button.LCLICK)  
                count += 1
                if count >= 400:
                    print('ERROR: hatching - run time over')
                    self.holdEnd([Direction(Stick.LEFT, 85), Direction(Stick.RIGHT, 180)])
                    return False
            # end run
            # TOM_COMMENT 遅延対策 START
            self.wait(1.5)
            # TOM_COMMENT 遅延対策 END
            self.holdEnd([Direction(Stick.LEFT, 85), Direction(Stick.RIGHT, 180)])
            self.hatched_egg_total += 1
            print('egg hatching: ',str(i+1),'/',eggs,' total: ',str(self.hatched_egg_total))
            while not self.checkMiniMapMarker():
                self.press(Button.A)   
            # reset direction
            self.wait(2)
            self.press(Button.L, wait=0.5) 
            self.wait(0.3)
        return True

    def pullEggs(self):
        '''
        タマゴを手持ちに移動
        【前提】ボックスを開いた状態
        【戻り値】int 手持ちのタマゴの数
        '''
        while True:
            print('_method_pullEggs') 
            # initialize
            eggs = 0     
            # open box
            self.openBox()                     
            # move box
            if self.moveBox('SV_AutoHatching\inbox_title_egg.png')  is None: 
                print('retry')
                # retry
                self.closeBox()
                continue    
            # party eggs check
            # TOM_COMMENT 特定（メテノ、コオリッポ）のポケモンの時は閾値を設ける
            #print('[DEGUG_pullEggs]party eggs check - tokupokeflag',self.tokupokeflag)
            if self.tokupokeflag:
                # if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],threshold=0.9,show_value=True):  
                if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],threshold=0.9):  
                    print('SKIP : pullEggs - already has eggs - tokupokeflag,',self.tokupokeflag)
                    eggs = self.checkPartyEggs()  
                    return eggs 
            else:
                # if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],show_value=True):  
                if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300]):  
                    print('SKIP : pullEggs - already has eggs')
                    eggs = self.checkPartyEggs()  
                    return eggs 
            # found eggs row 
            # TOM_COMMENT 特定（メテノ、コオリッポ）のポケモンの時は閾値を設ける
            #print('[DEGUG_pullEggs]found eggs row - tokupokeflag',self.tokupokeflag)
            if self.tokupokeflag:
                # position_egg = self.isContainTemplatePosition('SV_AutoHatching\inbox_egg.png',threshold=0.8,show_value=True)
                position_egg = self.isContainTemplatePosition('SV_AutoHatching\inbox_egg.png',threshold=0.8)
                # print('[debug]pullEggs - position_egg_get - tokupokeflag',self.tokupokeflag,'position_egg=',position_egg)
            else:
                # position_egg = self.isContainTemplatePosition('SV_AutoHatching\inbox_egg.png',show_value=True)
                position_egg = self.isContainTemplatePosition('SV_AutoHatching\inbox_egg.png')
                # print('[debug]pullEggs - position_egg_get','position_egg=',position_egg)
            if position_egg is None:
                print('SKIP : pullEggs - egg not found in boxs')
                return eggs
            # target column
            target_column = self.convertBoxColumn(position=position_egg)          
            # focus move   
            if not self.moveCellFocus(row=1,column=target_column) :
                print('retry')
                # LINE送信   
                if self.debug_img_display:
                    self.LINE_image('ERROR : pullEggs - moveCellFocus')    # デバッグ用：LINE通知不要なら削除
                # retry
                self.closeBox()
                continue
            # pull
            self.press(Button.MINUS, wait=0.3)
            self.press(Direction.DOWN, duration=1, wait=0.3)
            self.press(Button.A, wait=0.5)
            # focus                        
            self.pressRep(Direction.LEFT, target_column, interval=0.2)  
            self.moveCellFocus(row=2,column=0)           # 念のための処理（移動が失敗しやすいので位置をチェック）
            # put
            self.press(Button.A, wait=0.5)
            # party check
            # TOM_COMMENT 特定（メテノ、コオリッポ）のポケモンの時は閾値を設ける
            #print('[DEGUG_pullEggs]party check - tokupokeflag',self.tokupokeflag)
            if self.tokupokeflag:
                # if not self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],threshold=0.9,show_value=True):      
                if not self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],threshold=0.9):      
                    print('ERROR : pullEggs - cannot move eggs - tokupokeflag,',self.tokupokeflag)
                    # LINE送信   
                    if self.debug_img_display:
                        self.LINE_image('ERROR : pullEggs - cannot move eggs - tokupokeflag,',self.tokupokeflag)    # デバッグ用：LINE通知不要なら削除
                    # retry
                    self.closeBox()
                    continue    
            else:
                # if not self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],show_value=True):      
                if not self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300]):      
                    print('ERROR : pullEggs - cannot move eggs')
                    # LINE送信   
                    if self.debug_img_display:
                        self.LINE_image('ERROR : pullEggs - cannot move eggs')    # デバッグ用：LINE通知不要なら削除
                    # retry
                    self.closeBox()
                    continue    
            eggs = self.checkPartyEggs()   
            return eggs        
        
    def putHatchedEggs(self):
        '''
        孵化したポケモンをBOXに移動
        【戻り値】int 色違い数
        '''
        statuscheck_flag = False
        print('_method_putHatchedEggs')
        if self.mode == 2 :
            statuscheck_flag = True
        while True:
            # initialize
            shiny_count = 0
            count_move_box =0   
            # open box
            self.openBox()
            # party eggs check
            # TOM_COMMENT 特定（メテノ、コオリッポ）のポケモンの時は閾値を設ける
            #print('[DEGUG_putHatchedEggs]party eggs check - tokupokeflag',self.tokupokeflag)
            if self.tokupokeflag:
                if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300],threshold=0.9):  
                    print('SKIP : putHatchedEggs - already has eggs - tokupokeflag,',self.tokupokeflag)
                    self.wait(1)
                    return shiny_count            
            else:
                if self.isContainTemplate('SV_AutoHatching\inbox_egg.png',area=[0,720,0,300]):  
                    print('SKIP : putHatchedEggs - already has eggs')
                    self.wait(1)
                    return shiny_count            
            # party pkmn check                           
            if self.isContainTemplate('SV_AutoHatching\inbox_party_null_5.png',area=[0,720,0,300],threshold=0.9):
                print('SKIP : putHatchedEggs - already put pkmn')
                self.wait(1)
                return shiny_count            
            # move box
            if self.moveBox('SV_AutoHatching\inbox_title_egg.png')  is None:
                print('ERROR : putHatchedEggs - cannot move box')
                # retry
                self.closeBox()
                continue
            # party check 
            for i in range(1, 7):
                while not self.moveCellFocus(row=i,column=0):
                    print('ERROR : putHatchedEggs - moveCellFocus')
                    # send LINE
                    if self.debug_img_display:
                        self.LINE_image('ERROR : putHatchedEggs - moveCellFocus')    # デバッグ用
                    # retry
                    self.closeBox()
                    self.openBox()
                # cell check
                flag = self.checkCell(statuscheck_flag)
                if flag[0]: 
                    # shiny
                    shiny_count += 1
                    print('*** shiny(putHatchedEggs) ***')            
                    # if self.use_LINEnotice:
                    #     self.LINE_image('*** shiny(putHatchedEggs) ***')    # LINE通知不要なら削除 
                elif flag[1]:
                    # statusmatch
                    self.IV_flag = True    
                    print('*** status match ***')                
                    if self.use_LINEnotice:
                        self.LINE_image('*** status match ***')    # LINE通知不要なら削除  
            # find null row
            while True:
                position_null_space = self.isContainTemplatePosition('SV_AutoHatching\inbox_row_space.png',threshold=0.8,
                                                                        mask_path='SV_AutoHatching\mask_boxarea.png')
                if position_null_space is None:
                    # next box
                    self.press(Button.R, wait=0.8)
                    count_move_box +=1
                else:
                    column = self.convertBoxColumn(position=position_null_space)
                    break 
            # pull
            self.press(Direction.DOWN, duration=0.3, wait=0.2)      # 念のための処理（一番下を選択するようにする）
            self.press(Button.MINUS, wait=0.3) 
            while not self.moveCellFocus(row=2,column=0):            # 念のための処理（移動が失敗しやすいので位置チェックで対応）
                self.press(Direction.UP, duration=1, wait=0.3)
                self.press(Direction.DOWN, wait=0.5)
            self.press(Button.A, wait=0.5)
            # put
            self.press(Direction.UP, wait=0.3) 
            self.pressRep(Direction.RIGHT, column, interval=0.2, wait=0.3) 
            self.moveCellFocus(row=1,column=column)                  # 念のための処理（移動が失敗しやすいので位置をチェック）
            self.press(Button.A, wait=0.3)
            # party check                           
            if not self.isContainTemplate('SV_AutoHatching\inbox_party_null_5.png',area=[0,720,0,300]):
                print('ERROR : putHatchedEggs - cannot move pkmn')
                # send LINE
                if self.debug_img_display:
                    self.LINE_image('ERROR : putHatchedEggs - cannot move pkmn')    # デバッグ用
                # retry
                self.closeBox() 
                continue
            # before box            
            self.pressRep(Button.L, count_move_box, interval=0.1) 
            self.moveCellFocus(row=2,column=column)                  # ボックス名が見える位置にフォーカスを移動
            return shiny_count


    def checkBox(self,release_flag=False,statuscheck_flag=False):
        '''
        色違い・良個体値のポケモンをチェック
        【前提】BOXを開いた状態から
        【戻り値】int 色違い数
        '''  
        print('_method_checkBox')     
        # open box
        self.openBox()
        # box move
        self.moveBox('SV_AutoHatching\inbox_title_egg.png')
        # check
        shiny_count = self.checkBoxShinyOrStatus(release_flag=release_flag,statuscheck_flag=statuscheck_flag,pkmnmove_flag=True)
        print('*** shiny total *** ',self.shiny_total + shiny_count,'/',self.shiny_max)       
        # close
        self.closeBox()
        return shiny_count
