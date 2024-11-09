from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
from Commands.Keys import Button, Direction, Stick
from logging import getLogger, DEBUG, NullHandler


class BDSP_util(ImageProcPythonCommandTrim):

    """
    --------------------------------------------------------------------------------------
    ###SV_util.pyからコピー###
    ポケモンSV用コマンド v1.2 Release.2023/2/25
    Copyright(c) 2023 mikan kato
    ◆改修内容
        ・checkMiniMapMarker　upper値調整
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

    def softReboot(self):
        """
        ソフトの再起動（ソフトウェアの起動確認メッセージ対応）
        """
        print("_method(BDSP_util)_softReboot")
        error_count = 0
        # reset
        self.press(Button.HOME, wait=2)
        self.press(Button.X)
        self.press(Button.A, wait=4.5)
        # TOM_COMMENT 待ち時間増加(遅延対策) bak:1.5
        self.press(Button.A, wait=5)
        # TOM_COMMENT 待ち時間増加(サブ垢はソフトを遊べるかチェックがはいるのですこし待つ) bak:5
        self.press(Button.A, wait=7.5)
        # repeat A
        while not self.isContainTemplate("BDSP_util\_loading.png"):
        # TOM_COMMENT 待ち時間増加(遅延対策) bak:0.5
            self.press(Button.A, wait=1.5)
            error_count += 1
            if error_count > 60:
                print("ERROR:softReboot - error_count count over")
                return False
        return True

    