from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
from Commands.Keys import Button, Direction, Stick
from logging import getLogger, DEBUG, NullHandler


class util_Switch_Poke(ImageProcPythonCommandTrim):

    """
    --------------------------------------------------------------------------------------
    ポケモンSwitch用コマンド v1.2 Release.20yy/mm/dd
    Copyright(c) 2024 tom dp
    ◆改修内容
        ・2024/9/15 ファイル名変更（util_SWSH_SV　→　util_Switch_Poke）
    --------------------------------------------------------------------------------------
    """

    def __init__(self, cam, gui=None):
        super().__init__(cam)
        self.cam = cam
        self.gui = gui

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.debug_img_display = False  # debug用 True=エラー時の画像をLINEに送信
        self.debug_messege_display = False  # debug用 True=処理確認用のメッセージをprint

    """
    --------------------------------------------------------------------------------------
    ソフトウェア再起動
    --------------------------------------------------------------------------------------
    """

    def softRebootSwitch(self):
        """
        ソフトの再起動（ソフトウェアの起動確認メッセージ対応）
        """
        print("_method(util_Switch_Poke)_softReboot")
        error_count = 0
        # reset
        self.press(Button.HOME, wait=2) #ホームに移動
        self.press(Button.X) #メニュー表示
        self.press(Button.A, wait=4.0) #終了する
        self.press(Button.A, wait=1.0)    #ゲーム選択
        self.press(Button.A, wait=2.0)  #ユーザ選択
        # 起動チェック中
        while self.isContainTemplate("check_soft.png", threshold=0.9):
            #何もしない
            self.wait(0.5)
        print("起動チェッククリア")
        # repeat A
        self.pressRep(Button.A, repeat=5, interval=0.5)
        # 画像認識処理繰り返し
        while True:
            # print("TEST：" + str(error_count))
            # self.wait(0.1)
            # 剣盾用処理
            if self.isContainTemplate("OP.png"):
                print("剣盾再起動OK")
                break
            # SV用処理
            if self.isContainTemplate("logo_game_freak.png"):
            # if self.isContainTemplate("_loading.png"):
            # if self.isContainTemplatePositionBGR(
            #     "_player_marker.png",
            #     threshold=0.7,
            #     mask_path="_mask_playermarker.png",
            #     lower=[0, 200, 200],
            #     upper=[8585, 255, 255],
            # ):
                print("ＳＶ再起動OK")
                break
            # エラー処理
            error_count += 1
            if error_count > 600:
                print("ERROR:softRebootSwitch - error_count count over")
                return False
        # 起動OK
        return True

