from .BDSP_util import BDSP_util
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat


class BDSP_util_box(BDSP_util):

    """
    --------------------------------------------------------------------------------------
    ###SV_util_box.pyからコピー###
     ポケモンSV用ボックス操作系コマンド v1.5 Release.2023/1/15
     Copyright(c) 2023 mikan kato
     ◆改修内容
        ・checkCellのフラグ誤りの修正
    --------------------------------------------------------------------------------------
    """

    def __init__(self, cam, gui=None):
        super().__init__(cam)
        self.cam = cam
        self.gui = gui

        self.use_LINEnotice = False  # LINE通知を使用する場合の変数  使用しないならFalseにしないとエラーになる
        self.debug_img_display = False  # debug用 True=エラー時の画像をLINEに送信（use_LINEnoticeがFalseだとTrueにしてもFalseとして処理されます）
        self.debug_messege_display = False  # debug用 True=処理確認用のメッセージをログに出力
        self.status = [[31, 31, 31, 31, 31, 31]]

    """
    --------------------------------------------------------------------------------------
    ボックス開閉
    --------------------------------------------------------------------------------------
    """

    def openBox(self):
        """        
        Xメニューを開いてボックスを選択する
        """
        print("_method(BDSP_util_box)_openBox")
        # check box open
        if self.isContainTemplate("SV_util\_box.png"):
            print("alrady opened Box")
            return
        # x menu
        self.openXmenu()
        # select box
        while not self.isContainTemplate("SV_util\_xmenu_focus_box.png"):
            self.press(Direction.DOWN, wait=0.5)
        # wait box
        while self.isContainTemplate("SV_util\_xmenu_focus_box.png"):
            self.press(Button.A, wait=1)
            self.wait(1)

    def closeBox(self):
        """
        ボックスを終了する
        """
        print("_method(SV_util_box)_closeBox")
        # check box open
        if self.isContainTemplate("SV_util\_box.png"):
            self.closeXmenu()
        else:
            print("ERROR: closeBox - box not open")
            self.closeXmenu()

    def moveBox(self, boxtitle_path):
        """
        指定のボックスまで移動する
        【前提】ボックスを開いた状態
        【戻り値】
            int:成功、ボックスを移動した回数
            None:ボックス無し

        Parameters
        ----------
        boxtitle_path : str
            開きたいボックス名の画像パスを渡す
        '''
        """
        print("_method(SV_util_box)_moveBox")
        # box move
        #print("DEBUG_0")
        for i in range(0, 30):
            #print("DEBUG_1")
            if not self.isContainTemplate(boxtitle_path):
                #print("DEBUG_2")
                self.press(Button.L, wait=0.3)
                print("move box")
            else:
                #print("DEBUG_3")
                return i
        #print("DEBUG_4")
        print("ERROR: moveBox - cannot found box")
        return None

    """
    --------------------------------------------------------------------------------------
    ボックス操作用関数
    --------------------------------------------------------------------------------------
    """

    def moveCellFocus(self, row, column):
        """
        ボックスのフォーカスを、指定の行列の位置に移動する
        【前提】ボックスを開いた状態
        【戻り値】
            True:成功
            False:フォーカスの認識に失敗

        Parameters
        ----------
        row : int
            移動したいボックスの行を渡す
        column : int
            移動したいボックスの列を渡す
        """
        move_count = 0
        area_row = self.convertBoxRow(row=row)
        area_column = self.convertBoxColumn(column=column)
        # debug message
        if self.debug_messege_display:
            print("_method(SV_util_box)_moveCellFocus row=", row, "column=", column)
        # focus move
        while True:
            # check background color
            cursor_position = self.isContainTemplatePositionBGR(
                "SV_util\_box_focus_cell_bg.png",
                threshold=0.8,
                lower=[0, 190, 200],
                upper=[80, 255, 255],
                mask_path="SV_util\_mask_boxarea_partyarea.png",
            )  # 環境に合わせてBGR値を設定ください
            # not found
            if cursor_position is None:
                # check background color (pull)
                cursor_position = self.isContainTemplatePositionBGR(
                    "SV_util\_box_focus_cell_bg_pull.png",
                    threshold=0.8,
                    lower=[0, 190, 200],
                    upper=[80, 255, 255],
                    mask_path="SV_util\_mask_boxarea_partyarea.png",
                )  # 環境に合わせてBGR値を設定ください
                # not found
                if cursor_position is None:
                    print("cursor_position not found  row=", row, "column=", column)
                    return False
            # count move
            move_count += 1
            if move_count > 40:
                print(
                    "ERROR : cursor_position move_count over row=",
                    row,
                    "column=",
                    column,
                )
                return False
            # move row
            if cursor_position[1] < area_row[0]:
                self.press(Direction.DOWN, wait=0.3)
            elif cursor_position[1] > area_row[1]:
                self.press(Direction.UP, wait=0.3)
            else:
                # move column
                if cursor_position[0] < area_column[0]:
                    self.press(Direction.RIGHT, wait=0.3)
                elif cursor_position[0] > area_column[1]:
                    self.press(Direction.LEFT, wait=0.3)
                else:
                    # move success
                    return True

    def moveCellFocusNext(self, now_row, now_column):
        """
        現在のセルから次のセルへ移動
        次のセル＝奇数行の場合右へ1つ、偶数行の場合左へ1つ、行の端の場合下へ1つ移動した位置
        【前提】ボックスを開いた状態から
        【戻り値】
            移動した場合:[int（行）,int（列）]
            次セルがない場合：None

        Parameters
        ----------
        now_row : int
            現在の行を渡す
        now_column : int
            現在の列を渡す
        """
        # focus count
        if now_column == 6 and now_row == 5:
            return [99, 99]
        elif now_column >= 6 and now_row % 2 != 0:
            # row move
            now_row += 1
            self.press(Direction.DOWN, wait=0.5)
        elif now_column <= 1 and now_row % 2 == 0:
            # row move
            now_row += 1
            self.press(Direction.DOWN, wait=0.5)
        elif now_row % 2 == 0:
            # column move
            now_column -= 1
            self.press(Direction.LEFT, wait=0.3)
        elif now_row % 2 == 1:
            # column move
            now_column += 1
            self.press(Direction.RIGHT, wait=0.3)
        return [now_row, now_column]

    """
    --------------------------------------------------------------------------------------
    座標/セル位置変換
    --------------------------------------------------------------------------------------
    """

    def convertBoxColumn(self, position=None, column=None):
        """
        座標位置<=>ボックスの列を変換して返す
        列0 : パーティ列
        列1~6 : ボックスの列
        列99 : 該当列無し

        Parameters
        ----------
        position : [int,int]
            [左,上]の座標位置を渡すと、座標位置がボックスの何列目かを返す
        column : int
            ボックスの列数を渡すと、その列の[左端,右端]の座標を返す
        """
        # initialize
        width = 84  # 1列の幅
        left_point = 301  # 1列目の左端
        # check
        if position is not None:
            # return column
            for countColumn in range(0, 7):
                if position[0] <= width * (countColumn) + left_point:
                    return countColumn
            return 99
        else:
            # return position
            if column <= 0:
                return [0, left_point - 1]
            return [
                width * (column - 1) + left_point,
                width * (column) + left_point - 1,
            ]

    def convertBoxRow(self, position=None, row=None):
        """
        座標位置<=>ボックスの行を変換して返す
        行0 : ボックスより上
        行1~6 : ボックス・パーティの1行目から6行目
        行99 : 該当行無し

        Parameters
        ----------
        position : [int,int]
            [左,上]の座標位置を渡すと、座標位置がボックスの何行目かを返す
        row : int
            ボックスの行数を渡すと、その列の[上端,下端]の座標を返す
        """
        # initialize
        height = 84  # 1列の高さ
        top_point = 134  # 1列目の上端
        # check
        if position is not None:
            # return column
            for countRow in range(0, 7):
                if position[1] <= height * (countRow) + top_point:
                    return countRow
            return 99
        else:
            # return position
            if row <= 0:
                return [0, top_point - 1]
            return [height * (row - 1) + top_point, height * (row) + top_point]

    """
    --------------------------------------------------------------------------------------
    空きセル取得
    --------------------------------------------------------------------------------------
    """

    def findNullCell(self):
        """
        空いているセルの場所を返す
        【前提】ボックスを開いた状態から
        【戻り値】
            セルがある場合：[int（行）,int（列）]
            セルがない場合：None
        """
        for row in range(1, 6):
            area_row = self.convertBoxRow(row=row)
            for column in range(1, 7):
                area_column = self.convertBoxColumn(column=column)
                target_area = [area_row[0], area_row[1], area_column[0], area_column[1]]
                # check null
                if self.isContainTemplate(
                    "SV_util\_box_cell_null.png", area=target_area
                ):
                    return [row, column]
        return None

    """
    --------------------------------------------------------------------------------------
    逃がし
    --------------------------------------------------------------------------------------
    """

    def releasePkmn(self):
        """
        逃がす処理
        【前提】対象のポケモンにカーソルをあてた状態から
        """
        status_lv_area = [0, 100, 1120, 1280]
        # target is not null
        if self.isContainTemplate("SV_util\_box_status_lv.png", area=status_lv_area):
            while True:
                self.press(Button.A, wait=0.5)
                if self.isContainTemplate("SV_util\_box_message_pkmnmenu.png"):
                    break
            while True:
                self.press(Direction.UP, wait=0.3)
                if self.isContainTemplate(
                    "SV_util\_box_pkmnmenu_nigasu.png", use_gray=False, threshold=0.8
                ):
                    break
            while True:
                self.press(Button.A, wait=1)
                if self.isContainTemplate("SV_util\_box_pkmnmenu_no.png"):
                    break
            while True:
                self.press(Direction.UP, wait=0.3)
                if not self.isContainTemplate("SV_util\_box_pkmnmenu_no.png"):
                    break
            while True:
                self.press(Button.A, wait=0.3)
                if not self.isContainTemplate(
                    "SV_util\_box_status_lv.png", area=status_lv_area
                ):
                    break
            self.wait(0.5)

    """
    --------------------------------------------------------------------------------------
    ポケモンの移動（タマゴ以外）
    --------------------------------------------------------------------------------------
    """

    def putNextBox(self):
        """
        次以降のボックスの空きセルにポケモンを移動する
        【前提】動かしたいポケモンにフォーカスがある状態から
        """
        print("_method_putNextBox")
        # initialize
        count_move_box = 0
        # pull
        while not self.isContainTemplate("SV_util\_box_pullPkmn.png"):
            self.press(Button.Y, wait=0.5)
        # next box
        while True:
            self.press(Button.R, wait=0.8)
            count_move_box += 1
            # find null cell
            target_area = self.findNullCell()
            if target_area is not None:
                break
        # focus move
        if self.moveCellFocus(row=target_area[0], column=target_area[1]) == False:
            self.press(Button.B, wait=0.5)
            print("ERROR: putNextBox - connot moved pkmn")
            return False
        self.press(Button.A, wait=1)
        # before box
        self.pressRep(Button.L, count_move_box, interval=0.1)
        return True

    """
    --------------------------------------------------------------------------------------
    任意ステータス確認
    --------------------------------------------------------------------------------------
    """

    def checkCell(self, statuscheck_flag=False):
        """
        セルにいるポケモンが色違い/任意ステータスか確認する
        【前提】対象のポケモンにカーソルをあてた状態から
        """
        # debug message
        if self.debug_messege_display:
            print("_method(SV_util_box)_checkCell")
        shiny_flag = False
        status_flag = False
        # cell check
        if self.isContainTemplate(
            "SV_util\_box_status_lv.png", area=[0, 100, 1100, 1280]
        ):
            # shiny check
            if self.isContainTemplate(
                "SV_util\_shiny_mark.png", area=[0, 100, 1100, 1280]
            ):
                shiny_flag = True
            else:
                if statuscheck_flag:
                    # status check
                    statuscheck_result = self.checkCellPkmnStatus()
                    if statuscheck_result:
                        status_flag = True
        return [shiny_flag, status_flag]

    """
    --------------------------------------------------------------------------------------
    任意ステータス確認
    --------------------------------------------------------------------------------------
    """

    def checkCellPkmnStatus(self):
        """
        ジャッジ機能を開き、ステータスチェックを行う
        self.statusで設定した数分チェック処理を呼び出す
        【前提】対象のポケモンにカーソルをあてた状態から
        """
        # debug message
        if self.debug_messege_display:
            print("_method(SV_util_box)_checkCellPkmnStatus")
        # mode
        while not self.isContainTemplate("SV_util\_box_mode_judge.png"):
            self.press(Button.PLUS, wait=0.5)
        # status check
        for l in range(0, len(self.status)):
            if self.checkStatus(status=self.status[l]):
                return True
        return False

    def checkStatus(self, status=[31, 31, 31, 31, 31, 31]):
        """
        指定値のV/逆Vかどうか確認
        【前提】対象のポケモンにカーソルをあて、ジャッジ技能を表示した状態から
        """
        area_h = [140, 191, 835, 1280]
        area_a = [192, 258, 1061, 1280]
        area_b = [259, 325, 1061, 1280]
        area_c = [192, 258, 835, 1060]
        area_d = [259, 325, 835, 1060]
        area_s = [326, 380, 835, 1280]
        statusArea = [area_h, area_a, area_b, area_c, area_d, area_s]
        for i in range(0, 6):
            # V check
            if status[i] == 31 and not self.isContainTemplate(
                "SV_util\_box_status_31.png", area=statusArea[i]
            ):
                return False
            # 0 check
            elif status[i] == 0 and not self.isContainTemplate(
                "SV_util\_box_status_0.png", area=statusArea[i]
            ):
                return False
        return True

    """
    --------------------------------------------------------------------------------------
    ボックス内のポケモンの色/個体値を順番にチェック
    --------------------------------------------------------------------------------------
    """

    def checkBoxShinyOrStatus(
        self, release_flag=False, statuscheck_flag=False, pkmnmove_flag=False
    ):
        """
        色違い・良個体値のポケモンをチェック（戻り値あり）
        【前提】BOXを開いた状態から
        """
        print("_method(SV_util_box)_checkBoxShinyOrStatus")
        print(
            "release_flag : ",
            release_flag,
            " / statuscheck_flag : ",
            statuscheck_flag,
            " / pkmnmove_flag : ",
            pkmnmove_flag,
        )
        # initialize
        now_row = 1
        now_column = 1
        shiny_count = 0
        # open box
        self.openBox()
        # check
        while True:
            # focus check and move
            if not self.moveCellFocus(row=now_row, column=now_column):
                print("ERROR : checkBoxShinyOrStatus - moveCellFocus")
                # send LINE
                if self.debug_img_display:
                    self.LINE_image(
                        "ERROR : checkBoxShinyOrStatus - moveCellFocus"
                    )  # デバッグ用：LINE通知不要なら削除
                # retry
                now_row = 1
                now_column = 1
                self.closeBox()
                self.openBox()
                continue
            # cell check (shiny or statusmatch)
            flag = self.checkCell(statuscheck_flag=statuscheck_flag)
            if flag[0]:
                # shiny
                shiny_count += 1
                print("*** ★★★shiny★★★ ***")
                # send LINE
                if self.use_LINEnotice:
                    self.LINE_image("*** shiny ***")  # LINE通知不要なら削除
                if pkmnmove_flag:
                    self.putNextBox()  # 次のボックスにポケモンを移動する
                    continue
            elif flag[1]:
                # statusmatch
                self.IV_flag = True
                print("*** status match ***")
                if self.use_LINEnotice:
                    self.LINE_image("*** status match ***")  # LINE通知不要なら削除
                if pkmnmove_flag:
                    self.putNextBox()  # 次のボックスにポケモンを移動する
                    continue
            elif release_flag:
                # release
                self.releasePkmn()
            # next focus
            now_row, now_column = self.moveCellFocusNext(now_row, now_column)
            # last cell
            if now_row >= 6:
                break
        # flag check
        if shiny_count <= 0:
            print("*** not shiny ***")
            # send LINE
            #comment 不要
            #if self.debug_img_display:
                #self.LINE_image("*** not shiny ***")  # デバッグ用：LINE通知不要なら削除
        return shiny_count
