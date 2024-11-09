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

        self.shiny_max = 1                      # 色違い取得最大数を指定するための変数  色違い取得後にレポートを書かないようにしたい場合は1にします
        self.shiny_total = 0        # 色違い取得数をカウントするための変数

    def do(self):
        print(datetime.datetime.now())
        print(Test.__qualname__)
        self.EXExPrint("EXExPrint：テストメッセージ", debug_flag=True)
        self.EXExPrint("EXExGetTemplPass：" + self.EXExGetTemplPass("test01.png"))

    # メッセージ出力
    def EXExPrint(self, msg, line_flag=False, debug_flag=False):
        super().EXExPrint("T", msg, line_flag, debug_flag)

    # Templateパス取得
    # 引数１：画像ファイル名
    # 戻り値：self.tmplFolder＋"\"＋file ※例）EXE2\_test.png
    def EXExGetTemplPass(self, file):
        return super().EXExGetTemplPass("Test", file)