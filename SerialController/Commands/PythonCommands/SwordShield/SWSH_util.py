from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
from Commands.Keys import Button, Direction, Stick
from logging import getLogger, DEBUG, NullHandler


class SWSH_util(ImageProcPythonCommandTrim):

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
        print("_method(SWSH_util)_softReboot")
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
        while not self.isContainTemplate("SV_util\_loading.png"):
        # TOM_COMMENT 待ち時間増加(遅延対策) bak:0.5
            self.press(Button.A, wait=1.5)
            error_count += 1
            if error_count > 60:
                print("ERROR:softReboot - error_count count over")
                return False
        return True

    """
    --------------------------------------------------------------------------------------
    Xメニュー操作用関数
    --------------------------------------------------------------------------------------
    """

    def openXmenu(self):
        """
        Xメニューを開く
        """
        # x menu
        while not self.isContainTemplate(
            "SV_util\_xmenu.png", use_binary=True, threshold_binary=190
        ):
            # open
            if self.checkMiniMapMarker():
                self.press(Button.X, wait=1)
            else:
                self.press(Button.B, wait=0.5)
        self.press(Direction.RIGHT)

    def closeXmenu(self):
        """
        Xメニューを終了する
        """
        print("_method(SV_util)_closeXmenu")
        # xmenu close
        while not self.checkMiniMapMarker():
            self.press(Button.B, wait=2)
        self.wait(0.5)
        return

    def report(self):
        """
        レポートを書く
        """
        self.openXmenu()
        self.press(Button.R, wait=1)
        self.pressRep(Button.A, repeat=2, interval=0.5)
        self.wait(3)
        self.pressRep(Button.B, repeat=5, interval=0.5)

    """
    --------------------------------------------------------------------------------------
    フィールド画面確認
    --------------------------------------------------------------------------------------
    """

    def checkMiniMapMarker(self):
        """
        フィールド画面になっていることをミニマップの表示で確認する
        【戻り値】bool
            True：ミニマップ（プレーヤーマーカー）あり
            False：表示なし
        """
        if self.isContainTemplatePositionBGR(
            "SV_util\_player_marker.png",
            threshold=0.7,
            mask_path="SV_util\_mask_playermarker.png",
            lower=[0, 200, 200],
            upper=[8585, 255, 255],
        ):
            return True
        return False

    """
    --------------------------------------------------------------------------------------
    そらをとぶ
    --------------------------------------------------------------------------------------
    """

    def resetPosition(self, target_path):
        """
        Yメニューを開き、空を飛んでポジションリセットする
        【戻り値】bool
        True:成功
        False:エラーあり

        Parameters
        ----------
        target_path : str
            目的地名の画像パスを渡す
        """
        count = 0
        retry_count = 0
        print("_method(SV_util)_resetPosition")
        # open map
        while not self.isContainTemplate("SV_util\_ymenu_map.png"):
            self.press(Button.Y, wait=2)
            retry_count += 1
            if retry_count > 10:
                return False
        # move cursor
        while True:
            if self.isContainTemplate(target_path):
                break
            count += 1
            if count == 1:
                self.press(Direction(Stick.LEFT, 0, 0.2), duration=0.2)
                self.wait(0.5)
            elif count == 2:
                self.press(Direction(Stick.LEFT, 180, 0.2), duration=0.2)
                self.wait(0.5)
            elif count == 3:
                self.press(Direction(Stick.LEFT, -60, 0.2), duration=0.2)
                self.wait(0.5)
            else:
                # reset
                self.press(Button.PLUS, wait=0.5)
                count = 0
        # repeat A
        retry_count = 0
        while self.isContainTemplate(target_path):
            self.press(Button.A, wait=0.3)
            retry_count += 1
            if retry_count > 10:
                return False
        self.wait(5)
        # reset direction
        self.press(Button.L, wait=1.5)
        return True
