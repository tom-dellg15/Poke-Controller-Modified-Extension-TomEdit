from .SV_util import SV_util
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat


class SV_util_picnic(SV_util):

    '''
    --------------------------------------------------------------------------------------
     ポケモンSV用ピクニック操作系コマンド v1.3 Release.2023/1/15
     Copyright(c) 2023 mikan kato
     ◆改修内容
        ・_init_にdebugフラグを追加
        ・エラー時にLINEに画像を送信するよう変更（self.debug_img_display = Trueのとき）
        ・makeSandwichのパワー認識
        ・エラー時コメントの体裁修正（1/14）
    --------------------------------------------------------------------------------------
    '''
    def __init__(self,cam,gui=None):
        super().__init__(cam)
        self.cam = cam
        self.gui = gui

        self.use_LINEnotice = False              # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになる
        self.debug_img_display = False           # debug用 True=エラー時の画像をLINEに送信（use_LINEnoticeがFalseだとTrueにしてもFalseとして処理されます）
        self.debug_messege_display = False      # debug用 True=処理確認用のメッセージをログに出力
            

    '''
    --------------------------------------------------------------------------------------
     ピクニックの開閉
    --------------------------------------------------------------------------------------
    '''

    def openPicnic(self):
        """        
        Xメニューを開いてピクニックを選択する
        """
        print('_method(SV_util_picnic)_openPicnic')
        # reset direction
        self.press(Direction.DOWN, duration=0.2, wait=0.5)  
        # x menu
        self.openXmenu()  
        # select picnic
        while not self.isContainTemplate('SV_util\_xmenu_focus_picnic.png'):
            self.press(Direction.DOWN, wait=0.5)    
        self.press(Button.A, wait=7) 
        # close Miraidon
        self.press(Button.PLUS, wait=5)    


    def closePicnic(self):
        """
        ピクニックを終了する
        ※ピクニック終了時のレベルアップ挙動終了の確認のためXメニューを開く
        """
        print('_method(SV_util_picnic)_closePicnic')
        # close
        while self.isContainTemplate('SV_util\_picnic_endcommand.png'):
            self.press(Button.Y, wait=0.5)  
            self.press(Button.A, wait=0.7)  
            self.press(Button.A, wait=0.7)  
        self.wait(1)
        # skip lvup message
        # x menu
        while not self.isContainTemplate('SV_util\_xmenu.png',use_binary=True, threshold_binary=190):   
            self.press(Button.B, wait=0.5)  
            self.press(Button.X, wait=1)  
        self.closeXmenu()
        

    '''
    --------------------------------------------------------------------------------------
     料理
    --------------------------------------------------------------------------------------
    '''    
    def makeSandwich(self,recipe_path,power_path,repeatcount_max=30):
        """
        サンドイッチを作って食べる
        【前提】テーブルに向かった状態で、レシピが具材1つだけのもの
        【戻り値】bool
            True:指定レシピで作成・パワーの発動ができた時
            False:エラーがあった時

        Parameters
        ----------
        recipe_path : str
            使用したいレシピ名画像のパスを渡す
        power_path: : str
            発動を確認したいパワーのレベル画像のパスを渡す
        repeatcount_max : int
            レシピの検索上限を渡す（レシピを行き過ぎてしまったときに早めにやり直すための上限）
        """
        print('_method(SV_util_picnic)_makeSandwich')
        repeatcount = 0
        # start cook
        self.press(Button.A, wait=1)    
        self.press(Button.A, wait=6)  
        # check started cooking
        if not self.isContainTemplate('SV_util\_sandwich_recipetitle.png'):
            print('ERROR: makeSandwich -  cannot open recipe')
            # debug
            if self.debug_img_display:
                self.LINE_image('ERROR: makeSandwich - cannot open recipe') 
            return False
        # choice sandwich        
        while not self.isContainTemplate(recipe_path, threshold=0.9, area=[0,720,0,680]):
            self.press(Direction.RIGHT,wait=0.3)
            repeatcount+=1
            # error check
            if repeatcount > repeatcount_max:
                print('cannot found recipe')
                # cancel cooking 
                self.press(Button.B, wait=1)    
                self.press(Button.B, wait=1) 
                repeatcount = 0
                # start cook
                self.press(Button.A, wait=1)    
                self.press(Button.A, wait=6)    
        # submit
        self.pressRep(Button.A, repeat=2, interval=0.3)           
        self.wait(10)                                    # 微調整メモ：調理開始画面に入るのが早すぎる場合はwaitの時間を延ばしてください     
        # move topping
        for i in range(0, 3):
            self.press(Direction.UP, duration=0.5)  
            repeatcount = 0
            # cursor on topping
            while True:            
                # position adjustment
                position = self.isContainTemplatePosition('SV_util\_sandwich_cursor.png')
                if position is None:
                    self.press(Direction.DOWN,duration=0.005)
                elif position[1]>100:
                    self.press(Direction.UP,duration=0.005)
                elif position[1]<70:
                    self.press(Direction.DOWN,duration=0.005)
                else:
                    break
                # error check
                repeatcount+=1
                if repeatcount >15: 
                    print('ERROR: makeSandwich - cannot move to topping')
                    break
            self.hold(Button.A)
            # cursor on pan
            self.press(Direction.DOWN, duration=0.5) 
            repeatcount = 0
            while True:
                # position adjustment
                position = self.isContainTemplatePosition('SV_util\_sandwich_cursor.png')
                if position is None:
                    self.press(Direction.DOWN,duration=0.005)
                elif position[1]>320:
                    self.press(Direction.UP,duration=0.005)
                elif position[1]<295:
                    self.press(Direction.DOWN,duration=0.005)
                else:
                    break
                # error check
                repeatcount += 1
                if repeatcount > 15: 
                    print('ERROR: makeSandwich - cannot move to pan')
                    break
            if i==1:
                self.press(Direction.LEFT,duration=0.2, wait=0.3)
            elif i==2:
                self.press(Direction.RIGHT,duration=0.2, wait=0.3)
            self.holdEnd(Button.A)
            if i==1:
                self.press(Direction.RIGHT,duration=0.2, wait=0.3)
            elif i==2:
                self.press(Direction.LEFT,duration=0.2, wait=0.3)
        # wait power
        repeatcount = 0
        while not self.isContainTemplate('SV_util\_sandwich_power.png', use_binary=True, threshold_binary=190, mask_path='SV_util\_mask_picnic_sandwichpower.png'):
            self.press(Button.A,wait=0.5)
            repeatcount+=1
            if repeatcount >150:
                print('ERROR: makeSandwich - time over')
                # debug
                if self.debug_img_display:
                    self.LINE_image('ERROR: makeSandwich - makeSandwich time over')   
                return False
        self.wait(1)
        # check egg power
        if not self.isContainTemplate(power_path,threshold=0.8, use_binary=True, threshold_binary=190, mask_path='SV_util\_mask_picnic_sandwichpower.png'):
            print('ERROR: makeSandwich - sandwich power is not get')
            # debug
            if self.debug_img_display:
                self.LINE_image('ERROR: makeSandwich - sandwich power is not get')   
            return False
        # A repeat
        while not self.isContainTemplate('SV_util\_picnic_endcommand.png'):
            self.press(Button.A,wait=0.5)
        self.wait(2)
        return True

    '''
    --------------------------------------------------------------------------------------
     バスケットのチェック
    --------------------------------------------------------------------------------------
    '''    
            
    def checkBasket(self,egg=30):
        '''
        バスケット内のタマゴをチェック
        【前提】バスケットに向いた状態
        【戻り値】bool
            True:指定数タマゴを取得できた時　※たまに指定数以下になる時があります
            False:タマゴが見つからなかった時

        Parameters
        ----------
        egg : int
            取得したいタマゴ数を設定すると、その数分バスケットからタマゴを取得する
        '''
        print('_method(SV_util_picnic)_checkBasket')
        egg_count=0
        wait_count = 0
        # check basket
        self.press(Button.A,wait=1) 
        if not self.isContainTemplate('SV_util\_picnic_message_basket_check.png'):
            print('ERROR: checkBasket - cannot walk to basket')
            # debug
            if self.debug_img_display:
                self.LINE_image('ERROR: checkBasket - cannot walk to basket')  
            return False
        # repeat check basket    
        while True:
            # egg found message
            if self.isContainTemplate('SV_util\_picnic_message_egg_found.png',threshold=0.9):
                wait_count = 0
                if egg_count<egg:
                    # get egg
                    egg_count += 1
                    print('egg found：',egg_count)
                    self.press(Button.A,wait=0.7)  
                    self.press(Button.A,wait=0.7)  
                else:
                    # don't get
                    self.press(Button.B,wait=0.5)  
                    self.press(Button.B,wait=0.5)  
            # egg not found message
            elif self.isContainTemplate('SV_util\_picnic_message_egg_notfound.png'):
                wait_count += 1
                if wait_count >= 10:             # 10bak   
                    print('ERROR: checkBasket - checkBasket time over')
                    # debug
                    if self.debug_img_display:
                        self.LINE_image('ERROR: checkBasket - checkBasket time over') 
                    return False
                # skip messsage
                self.press(Button.B,wait=0.5)
                if egg_count>=egg:
                    # egg max
                    break
                else:
                    # wait　！国際孵化でないと産まれる速度が著しく遅くなるので要注意！
                    self.wait(20) 
                    self.wait(20)   # 追加
                    self.wait(20)   # 追加
                    # タマゴパワー	時間目安
                    # なし	遅いときは約30〜40分かかることも
                    # Lv1	約2〜3分でタマゴが1個できる
                    # Lv2   約30秒でタマゴが1個できる
                    # Lv3	約15〜30秒でタマゴが1個できる
            else:
                # message skip
                self.press(Button.A,wait=0.6)  
        return True
