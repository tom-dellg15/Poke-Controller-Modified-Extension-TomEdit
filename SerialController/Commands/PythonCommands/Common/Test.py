from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
import time
import datetime
import tkinter
import tkinter.simpledialog as simpledialog

from Commands.PythonCommands.ScarletViolet.SV_util_box_Eng import SV_util_box_Eng
from Commands.PythonCommands.ScarletViolet.SV_util_picnic_Eng import SV_util_picnic_Eng
from ..Common.util_Switch_Poke import util_Switch_Poke
from ..RockmanEXE.EXE_util import EXE_util

from Commands.Keys import KeyPress, Button, Direction, Stick, Hat

class Test(SV_util_box_Eng,SV_util_picnic_Eng,util_Switch_Poke,EXE_util):
    NAME = '【共通】テスト'
    '''
    --------------------------------------------------------------------------------------
     テスト Release.2024/4/13
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

        self.shiny_max_default = 1  # 色違い取得最大数を指定するための変数 色違い取得後にレポートを書かないようにしたい場合は1にします
        self.shiny_max = 0          # 色違い取得最大数を指定するための変数 txtファイルor画面入力した値を保持する
        self.shiny_total = 0        # 色違い取得数をカウントするための変数

    def do(self):
        print(datetime.datetime.now())
        print(Test.__qualname__)
        # self.EXExPrint("EXExPrint：テストメッセージ", debug_flag=True)
        # self.EXExPrint("EXExGetTemplPass：" + self.EXExGetTemplPass("test01.png"))
        self.tkinterTest()

    # メッセージ出力
    def EXExPrint(self, msg, line_flag=False, debug_flag=False):
        super().EXExPrint("T", msg, line_flag, debug_flag)

    # Templateパス取得
    # 引数１：画像ファイル名
    # 戻り値：self.tmplFolder＋"\"＋file ※例）EXE2\_test.png
    def EXExGetTemplPass(self, file):
        return super().EXExGetTemplPass("Test", file)

############################################
    def tkinterProcess(self):
        import tkinter as tk
        import os
        import inspect

        print(inspect.currentframe().f_code.co_name + "開始")

        # txt読み込み
        pathword1 = os.getcwd()
        pathword2 = "profiles"
        pathword3 = self.profilename
        filename = "shiny_max_history.txt"
        path = os.path.join( pathword1, pathword2, pathword3, filename)
        try:
            f = open(path, "r")
            line = f.readline().rstrip()
            # 色違い取得最大数
            self.shiny_max = int(line)
            f.close()
        except Exception as e:
            print(e)
            print("決定ボタン押したら「" + path + "」を新規作成します")

        # ボタン処理
        def get_entry():
            # 色違い取得最大数
            self.shiny_max = int(entryShinyMax.get())
            # txt書込み
            with open(path, "w") as f:
                f.write(str(self.shiny_max))
                # self.print_t("書込み完了：" + str(self.shiny_max))
            self.pokemon_parent = entryPokeName.get()
            root.destroy()

        # エリア設定
        root = tk.Tk()
        root.title('Entry')
        root.geometry( '300x300' + '+1280+540' )

        # 入力ボックス：孵化するポケモン名
        entryPokeName = tk.Entry(root, width=20)
        # 初期値を入れておく
        entryPokeName.insert(0, "孵化するポケモン名をココに入力")
        entryPokeName.pack(pady=10)

        # 入力ボックス：色違い取得最大数
        entryShinyMax = tk.Entry(root, width=20)
        # 初期値を入れておく
        if self.shiny_max == 0 :
            self.shiny_max = self.shiny_max_default
        entryShinyMax.insert(0, self.shiny_max)
        entryShinyMax.pack(pady=10)

        # ボタン：決定
        button = tk.Button(root, text='決定', command=get_entry)
        button.pack()

        root.mainloop()
        
        print(inspect.currentframe().f_code.co_name + "終了")
        ############################################