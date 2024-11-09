from Commands.Keys import Button, Direction,Stick
from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
from .SV_util_box import SV_util_box


# 自動にがし
class ReleaseBox_pkmnSV(SV_util_box,ImageProcPythonCommandTrim):
    NAME = '【ＳＶ】自動リリース'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  
        self.cam = cam
        self.gui = gui             
        '''
        ◆◆◆事前設定◆◆◆
        下記の変数を設定する。0、31、99=任意
            6Vの場合        [31,31,31,31,31,31]
            A抜け5Vの場合   [31,0,31,31,31,31]または[31,99,31,31,31,31]
            S抜け5Vの場合   [31,31,31,31,31,0]または[31,31,31,31,31,99]
        '''
        # [H,A,B,C,D,S]の順で、残しておきたい個体値を配列型で列挙する（0、31、99=任意）
        self.status = [[31,31,31,31,31,31],[31,0,31,31,31,31],[31,31,31,31,31,0],[31,31,31,0,31,31]]
        
        self.boxs = 1                           # チェックするボックス数
        self.release_flag = True                # 逃がす処理をするか（True=する）
        self.statuscheck_flag = True            # ステータスチェックをするか（True=する）
        
        # 通知設定
        self.use_LINEnotice = True              # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになる
        self.debug_img_display = True           # debug用 True=エラー時の画像をLINEに送信（use_LINEnoticeがFalseだと、TrueにしてもFalseとして処理されます）
        self.debug_messege_display = False      # debug用 True=処理確認用のメッセージをログに出力

        self.shiny_total = 0                    # 色違い合計数カウンタ

    def do(self):          
        '''
        ボックス内のポケモンをチェックし、指定のステータス・色違い以外のポケモンを逃がす
        【前提】BOXを開いた状態の左上にフォーカスした状態からスタート
        '''
        print("---------------------------------------")
        print("自動リリース(SV)v1.3 Release.2023/1/10")
        print("Copyright(c) 2023 mikan kato")
        print("------------------------------------")
        if not self.use_LINEnotice:
            self.debug_img_display = False           # debug用 True=エラー時の画像をLINEに送信
        for i in range(0, self.boxs):
            print("------------------------------------")
            self.checkBoxShinyOrStatus(release_flag=self.release_flag,statuscheck_flag=self.statuscheck_flag)
            if i < self.boxs - 1:
                # next box
                self.press(Button.R, wait=0.5)
        return
                
