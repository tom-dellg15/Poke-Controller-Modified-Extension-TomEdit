import copy
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from logging import getLogger, DEBUG, NullHandler
from .EXE_util import EXE_util

class EXE2_util(EXE_util):

    """
    --------------------------------------------------------------------------------------
     ロックマンエグゼ２用コマンド v1.0 Release.2024/10/12
     Copyright(c) 2024 tom dp
     ◆改修内容
        ・
        ・
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

        ###シリーズ固有値###
        self.seriesNumber = "2" #ナンバリング
        self.tmplFolder = "EXE2" #Templateフォルダ名
        self.max_row = 2    #カスタム画面の最大行数
        self.max_col = 5    #カスタム画面の最大列数
        self.normal_end = "E200"  #正常終了
        self.error_nochip_backpack = "E211" #通信対戦エラー（負けた時に相手に渡すチップがない）
        self.sytem_code = self.normal_end   #エラー処理用
        self.result_processing_flag = False #リザルト画面処理中フラグ

        ###実装側で変更可能####
        # self.xxxx = vvvv

    """
    --------------------------------------------------------------------------------------
    @abstractmethod -> overload
    --------------------------------------------------------------------------------------
    """
    # メッセージ出力
    def EXExPrint(self, msg, line_flag=False, debug_flag=False):
        super().EXExPrint(self.seriesNumber, msg, line_flag, debug_flag)

    """
    --------------------------------------------------------------------------------------
    @abstractmethod -> overload
    --------------------------------------------------------------------------------------
    """
    # Templateパス取得
    # 引数１：画像ファイル名
    # 戻り値：self.tmplFolder＋"\"＋file ※例）EXE2\_test.png
    def EXExGetTemplPass(self, file):
        return super().EXExGetTemplPass(self.tmplFolder, file)

    """
    --------------------------------------------------------------------------------------
    ログにエラー出力する
    --------------------------------------------------------------------------------------
    """
    # ログにエラー出力する
    # 引数１：LINE通知フラグ
    def EXE2Error(self, line_flag):
        '''
        【概要】ログにエラー出力
        【前提】＠ｄｓｄｄｄ＠
        rtype
        ----------

        Parameters
        ----------
        line_flag : LINE通知フラグ
        '''
        if self.sytem_code == self.normal_end :
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(self.winner_flag)
                        +"正常終了"
                    , line_flag
                )
        elif self.sytem_code == self.error_nochip_backpack :
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(self.winner_flag)
                        + "通信対戦エラー（負けた時に相手に渡すチップがありません）"
                    , line_flag
                )
        else :
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(self.winner_flag)
                    + "未知のエラー発生"
                , line_flag
            )

    """
    --------------------------------------------------------------------------------------
    対人戦リザルト画面処理
    --------------------------------------------------------------------------------------
    """
    # 対人戦リザルト画面処理
    def EXE2PvpResult(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        # wait_flag = False
        self.result_processing_flag = False
        
        if winner_flag :
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_winner.png")
        else:
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_loser.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            self.press(Button.A, wait=0.5)
            self.battle_count += 1
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + str(self.battle_count) + "回目のバトル終了"
            )
            self.regularChip_used_flag = False
            self.wait(2)
            # wait_flag = True
            self.result_processing_flag = True

        # 敗者処理
        if not winner_flag :
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_loser_nochip_backpack.png")
            # エラー発生
            if self.isContainTemplate(templatePass, threshold=0.9):
                self.sytem_code = self.error_nochip_backpack
            #隠しチップ判定
            if self.result_processing_flag :
                self.EXE2HiddenChipJudge(winner_flag)

        # リザルト画面表示した場合はしばらく待つ
        # if wait_flag :
        if self.result_processing_flag :
            self.wait(4)

    """
    --------------------------------------------------------------------------------------
    隠しチップ判定
    --------------------------------------------------------------------------------------
    """
    # 隠しチップ判定
    def EXE2HiddenChipJudge(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        # Templateパス取得
        templatePass = self.EXExGetTemplPass("_battle_result_loser_nodata.png")
        if self.isContainTemplate(templatePass, threshold=0.95):
            # LINE通知
                self.LINE_image(self.EXExGetSeriesTag(self.seriesNumber) 
                    + self.EXExGetVictoryDefeatPlayer(winner_flag) +"隠しチップ発生") 

    """
    --------------------------------------------------------------------------------------
    対人戦リトライ処理
    --------------------------------------------------------------------------------------
    """
    # 対人戦リトライ処理
    def EXE2PvpRetry(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        if winner_flag :
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_winner_recieve.png")
        else:
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_loser_retry.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            #再戦選択
            self.press(Button.A, wait=0.5)

    """
    --------------------------------------------------------------------------------------
    対人戦ドロー処理（タイムアウト）
    --------------------------------------------------------------------------------------
    """
    # 対人戦ドロー処理（タイムアウト）
    def EXE2PvpResultDraw(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        templatePass = self.EXExGetTemplPass("_battle_result_draw_timeout.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "タイムアウト発生"
            )
            self.press(Button.A, wait=0.5)
            self.regularChip_used_flag = False
    
    """
    --------------------------------------------------------------------------------------
    対人戦ドロー処理（ネットワークメニューに戻る）
    --------------------------------------------------------------------------------------
    """
    # 対人戦ドロー処理（ネットワークメニューに戻る）
    def EXE2PvpResultToNetWorkMenu(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        templatePass = self.EXExGetTemplPass("_battle_result_draw_goto_networkmenu.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "ネットワークメニュー画面に戻る"
            )
            self.press(Button.A, wait=0.5)
            self.regularChip_used_flag = False

    """
    --------------------------------------------------------------------------------------
    ネットワーク画面処理
    --------------------------------------------------------------------------------------
    """
    #ネットワーク画面処理
    # 引数１：ホスト区分
    # 引数２：プレイヤー区分
    def EXE2NetWorkMenu(self, host_flag, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        #ネットバトルにカーソルが当たっているとき
        templatePass = self.EXExGetTemplPass("_network_netbattle.png")
        if self.isContainTemplate(templatePass, threshold=0.98):
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "ネットバトル選択"
                , debug_flag=True
            )
        
        #パブリックマッチにカーソルが当たっているとき
        templatePass = self.EXExGetTemplPass("_network_publicmatch.png")
        if self.isContainTemplate(templatePass, threshold=0.98):
            #ローカルマッチにカーソルが当たるまで移動
            templatePass = self.EXExGetTemplPass("_network_localmatch.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.press(Hat.BTM, wait=0.1)
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "ローカルマッチ選択"
                , debug_flag=True
            )
        
        #Nextにカーソルが当たっているとき（★もし未設定の場合はそのときロジックを組むか考える）
        templatePass = self.EXExGetTemplPass("_network_localmatch_next.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "Next選択"
                , debug_flag=True
            )
            
            #メッセージ選択が出るまで待機
            templatePass = self.EXExGetTemplPass("_network_msgselect.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "・・・コメント選択画面待機中・・・"
                ) 
                self.wait(5)
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "コメント選択"
                , debug_flag=True
                )
            
            #プレイヤーが認識されるまで待機
            if host_flag :
                templatePass = self.EXExGetTemplPass("_network_playerlist_winner.png")
            else :
                templatePass = self.EXExGetTemplPass("_network_playerlist_loser.png")
            templatePassSub = self.EXExGetTemplPass("_network_maching_continue.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "・・・マッチング中・・・"
                ) 
                self.wait(5)
                #対戦相手が見つからなかったときは継続
                if self.isContainTemplate(templatePassSub, threshold=0.9):
                    self.press(Button.A, wait=0.5)
                    self.EXExPrint(
                        self.EXExGetVictoryDefeatPlayer(winner_flag) 
                            + "・・・継続・・・"
                    ) 
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "プレイヤー選択"
                , debug_flag=True
            )
            
            #対戦申込を受けるまで待機
            if host_flag :
                templatePass = self.EXExGetTemplPass("_network_maching_response.png")
            else :
                templatePass = self.EXExGetTemplPass("_network_maching_request.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "・・・対戦申込待機中・・・"
                ) 
                self.wait(5)
            self.press(Button.A, wait=0.5)
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "対戦選択"
                , debug_flag=True
            )
            
            #マッチング完了し、即対戦画面へ
            self.logout_count = 0
            templatePass = self.EXExGetTemplPass("_battlescreen_start.png")
            while not self.isContainTemplate(templatePass, threshold=0.9):
                self.logout_count += 1
                if self.logout_count > 10:
                    self.EXExPrint(
                        self.EXExGetVictoryDefeatPlayer(winner_flag) 
                            + "・・・対戦画面待機中・・・"
                    ) 
                    self.logout_count = 0
                    self.regularChip_used_flag = False

    """
    --------------------------------------------------------------------------------------
    プレイヤー共通処理
    --------------------------------------------------------------------------------------
    """
    #プレイヤー共通処理
    # 引数１：プレイヤー区分
    def EXE2CustomScreenCommonLogic(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        if self.init_flag:
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "バトルオペレーション スタート！"
            )
    """
    --------------------------------------------------------------------------------------
    カスタム画面を開く
    --------------------------------------------------------------------------------------
    """
    #カスタム画面を開く
    # 引数１：プレイヤー区分
    def EXE2CustomScreenLoserLogic(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        templatePass = self.EXExGetTemplPass("_battlescreen_start.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            # プレイヤー共通処理
            self.EXE2CustomScreenCommonLogic(winner_flag)
            
            #カスタム画面を開いたらチップを何も選択せずOKボタンにカーソルを置く
            self.press(Button.PLUS, wait=0.5)

            #チップは何も選択せずにOK押下
            templatePass = self.EXExGetTemplPass("_battlescreen_nodata.png")
            if self.isContainTemplate(templatePass, threshold=0.9):
                self.press(Button.A, wait=0.5)
            
        #カスタムゲージが満タンになったらカスタム画面を開く
        templatePassP1 = self.EXExGetTemplPass("_battlescreen_fullcustum_p1.png")
        templatePassP2 = self.EXExGetTemplPass("_battlescreen_fullcustum_p2.png")
        if  ( self.isContainTemplate(templatePassP1, threshold=0.9) 
                or self.isContainTemplate(templatePassP2, threshold=0.9)
            ):
            self.press(Button.R, wait=0.5)

    """
    --------------------------------------------------------------------------------------
    チップ選択、実行
    --------------------------------------------------------------------------------------
    """
    #チップ選択、実行
    #前提：フルカスタムになったら敗者側がカスタム画面を開いてくれる前提
    #前提：プログラムアドバンス用のチップがレギュラーチップになっている事
    #前提：選択できるチップが10枚であること
    #条件：Regularチップ　可変対応
    # 引数１：プレイヤー区分
    # 引数２：認識対象チップ画像ファイル名のリスト
    # 引数３：引数２リスト内のレギュラーチップの要素数
    def EXE2CustomScreenWinnerLogic(self, winner_flag, chipArray, regular_Index):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        templatePass = self.EXExGetTemplPass("_battlescreen_start.png")
        if self.isContainTemplate(templatePass, threshold=0.9):
            # プレイヤー共通処理
            self.EXE2CustomScreenCommonLogic(winner_flag)

            # 前処理が残ったままここに来るとAボタン押下しチップ選択した状態になる可能性があるので、
            # Bボタンを数回押しておく
            self.press(Button.B, wait=0.1)
            self.press(Button.B, wait=0.1)
            self.press(Button.B, wait=0.1)
            
            #リスト内のチップ探索
            paChipArray = copy.deepcopy(chipArray) #深いコピー
            for i in range(0, len(chipArray)):
                #レギュラーチップかつ使用済の場合
                if ( i == regular_Index ) and ( not self._regularChip_used_flag ):
                    paChipArray[i] = [True, 0 , 0]
                #レギュラーチップ以外の場合
                else:
                    # 対象チップの位置探索
                    paChipArray[i] = self.EXExChipTargetSearch(chipArray[i])
                    # チップ初期位置リセット
                    self.EXExChipPosReset()

            #フルカスタム探索　
            fullcustumArray = self.EXExChipTargetSearch("_chip_fullcustum.png")
            # チップ初期位置リセット
            self.EXExChipPosReset()

            #プログラムアドバンスできる場合
            if paChipArray[0][0] and paChipArray[1][0] and paChipArray[2][0] :
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "プログラムアドバンス選択開始"
                    , debug_flag=True
                )
                #リスト内のチップ分ループ処理
                for i in range(0, len(paChipArray)) :
                    #チップ選択
                    self.EXExChipSelect(paChipArray[i][1], paChipArray[i][2], self.max_col)
                    #最後のチップは位置リセットしなくていい
                    if i < len(paChipArray) - 1 :
                        # チップ初期位置リセット
                        self.EXExChipPosReset()
                #OK
                self.EXExChipSelOK()
                # チップ実行
                self.EXExChipExecute(True, 8)
                # ここを通ったらレギュラーチップ使用した扱いとしておく
                self.regularChip_used_flag = True
            #フルカスタムがある場合
            elif fullcustumArray[0] :
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "フルカスタム選択開始"
                    , debug_flag=True
                )
                #フルカスタム選択
                self.EXExChipSelect(fullcustumArray[1], fullcustumArray[2], self.max_col)
                # チップ初期位置リセット
                self.EXExChipPosReset()
                # リスト内チップ、フルカスタム以外選択
                fileArray = chipArray.copy() #浅いコピー
                fileArray.append("_chip_fullcustum.png")
                self.EXExChipSelectOther(fileArray, 4)
                #OK
                self.EXExChipSelOK()
                # チップ実行
                self.EXExChipExecute(True, 3)
            #いずれも該当なければPA、フルカスタム以外のチップを選択してOK
            else:
                self.EXExPrint(
                    self.EXExGetVictoryDefeatPlayer(winner_flag) 
                        + "ＰＡ／フルカスタム以外選択開始"
                    , debug_flag=True
                )
                # リスト内チップ以外選択
                self.EXExChipSelectOther(chipArray, 5)
                #OK
                self.EXExChipSelOK()
                # チップ実行
                self.EXExChipExecute(True, 2)
