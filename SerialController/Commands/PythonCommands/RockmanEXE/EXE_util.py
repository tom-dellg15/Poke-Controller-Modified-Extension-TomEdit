import copy
from abc import ABC, abstractmethod
from Commands.PythonCommandBaseTrim import ImageProcPythonCommandTrim
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat 
from logging import getLogger, DEBUG, NullHandler

class EXE_util(ABC, ImageProcPythonCommandTrim):

    '''
    --------------------------------------------------------------------------------------
     ロックマンエグゼシリーズ共用コマンド v1.0 Release.2024/10/12
     Copyright(c) 2024 tom dp
     ◆改修内容
        ・
        ・
    --------------------------------------------------------------------------------------
    '''
    def __init__(self, cam, gui=None):
        super().__init__(cam)
        self.cam = cam
        self.gui = gui

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.normal_end = "Ex00"  #正常終了
        self.error_nochip_backpack = "Ex11" #通信対戦エラー（負けた時に相手に渡すチップがない）
        self.sytem_code = self.normal_end   #エラー処理用

        ###内部変数####
        self._regularChip_used_flag = False #レギュラーチップ使用有無
        self._pvpBattle_count_max = 0  # バトル最大回数 0以下：無限ループ　1以上：指定回数のみバトル処理ループ
        self.result_processing_flag = False #リザルト画面処理中フラグ

# ###################################################################################################################
# テスト中[EXE3]
    """
    --------------------------------------------------------------------------------------
    ローカルネットバトル本番処理
    --------------------------------------------------------------------------------------
    """
    def EXExLocalBattleReal(self, seriesNumber, winner_flag, host_flag, regular_Index, battle_count):
        '''
        【前提】前提条件を書きます
        【戻り値】合計バトル回数を返す
            True:ｘｘｘｘｘ
            False:ｙｙｙｙｙ

        Parameters
        ----------
        seriesNumber : str
        winner_flag : bool
        host_flag : bool
        regular_Index : int
        battle_count : int

        '''
        #ネットワーク画面処理
        self.EXExNetWorkMenu(host_flag, winner_flag)
        
        #リザルト画面判定
        battle_count = self.EXExPvpResult(seriesNumber, winner_flag, battle_count)

        #リトライ処理判定
        self.EXExPvpRetry(winner_flag)

        #カスタム画面処理（勝者）★ここは画像ファイル名を可変にする
        chipArray = [
                        "_chip_customsword.png"
                        , "_chip_varswrd.png" 
                        , "_chip_protomanV3.png"
                    ]
        # ★まだEXE3用にカスタマイズできていないので処理しない
        self.EXExCustomScreenWinnerLogic(winner_flag, chipArray, regular_Index)
        
        #ドロー（タイムアウト）
        self.EXExPvpResultDraw(winner_flag)

        #ドロー（ネットワークメニューに戻る）
        self.EXExPvpResultToNetWorkMenu(winner_flag)

        return battle_count
    """
    --------------------------------------------------------------------------------------
    ネットワーク画面処理
    --------------------------------------------------------------------------------------
    """
    #ネットワーク画面処理
    # 引数１：ホスト区分
    # 引数２：プレイヤー区分
    def EXExNetWorkMenu(self, host_flag, winner_flag):
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
    対人戦リザルト画面処理
    --------------------------------------------------------------------------------------
    """
    # 対人戦リザルト画面処理
    def EXExPvpResult(self, seriesNumber, winner_flag, battle_count):
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
            battle_count += 1
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + str(battle_count) + "回目のバトル終了"
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
                self.EXExHiddenChipJudge(seriesNumber, winner_flag)

        # リザルト画面表示した場合はしばらく待つ
        # if wait_flag :
        if self.result_processing_flag :
            self.wait(4)

        return battle_count
    """
    --------------------------------------------------------------------------------------
    隠しチップ判定
    --------------------------------------------------------------------------------------
    """
    # 隠しチップ判定
    def EXExHiddenChipJudge(self, seriesNumber, winner_flag):
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
                self.LINE_image(self.EXExGetSeriesTag(seriesNumber) 
                    + self.EXExGetVictoryDefeatPlayer(winner_flag) +"隠しチップ発生") 
    
    """
    --------------------------------------------------------------------------------------
    対人戦リトライ処理
    --------------------------------------------------------------------------------------
    """
    # 対人戦リトライ処理
    def EXExPvpRetry(self, winner_flag):
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
    チップ選択、実行  ★チップ選択画面で何枚選択できるか定義しておく必要あり（プログラム起動時に入力させよう）  
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
    def EXExCustomScreenWinnerLogic(self, winner_flag, chipArray, regular_Index):
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
            self.EXExCustomScreenCommonLogic(winner_flag)

            # 前処理が残ったままここに来るとAボタン押下しチップ選択した状態になる可能性があるので、
            # Bボタンを数回押しておく
            self.press(Button.B, wait=0.1)
            self.press(Button.B, wait=0.1)
            self.press(Button.B, wait=0.1)
            
            # ★チップ実行（ロックバスターを打つ）★
            self.press(Button.PLUS, wait=0.3)
            self.press(Button.A, wait=0.3)
            self.EXExChipExecute(False, 0)

            # #リスト内のチップ探索
            # paChipArray = copy.deepcopy(chipArray) #深いコピー
            # for i in range(0, len(chipArray)):
            #     #レギュラーチップかつ使用済の場合
            #     if ( i == regular_Index ) and ( not self._regularChip_used_flag ):
            #         paChipArray[i] = [True, 0 , 0]
            #     #レギュラーチップ以外の場合
            #     else:
            #         # 対象チップの位置探索
            #         paChipArray[i] = self.EXExChipTargetSearch(chipArray[i])
            #         # チップ初期位置リセット
            #         self.EXExChipPosReset()

            # #フルカスタム探索　
            # fullcustumArray = self.EXExChipTargetSearch("_chip_fullcustum.png")
            # # チップ初期位置リセット
            # self.EXExChipPosReset()

            # #プログラムアドバンスできる場合
            # if paChipArray[0][0] and paChipArray[1][0] and paChipArray[2][0] :
            #     self.EXExPrint(
            #         self.EXExGetVictoryDefeatPlayer(winner_flag) 
            #             + "プログラムアドバンス選択開始"
            #         , debug_flag=True
            #     )
            #     #リスト内のチップ分ループ処理
            #     for i in range(0, len(paChipArray)) :
            #         #チップ選択
            #         self.EXExChipSelect(paChipArray[i][1], paChipArray[i][2], self.max_col)
            #         #最後のチップは位置リセットしなくていい
            #         if i < len(paChipArray) - 1 :
            #             # チップ初期位置リセット
            #             self.EXExChipPosReset()
            #     #OK
            #     self.EXExChipSelOK()
            #     # チップ実行
            #     self.EXExChipExecute(True, 8)
            #     # ここを通ったらレギュラーチップ使用した扱いとしておく
            #     self.regularChip_used_flag = True
            # #フルカスタムがある場合
            # elif fullcustumArray[0] :
            #     self.EXExPrint(
            #         self.EXExGetVictoryDefeatPlayer(winner_flag) 
            #             + "フルカスタム選択開始"
            #         , debug_flag=True
            #     )
            #     #フルカスタム選択
            #     self.EXExChipSelect(fullcustumArray[1], fullcustumArray[2], self.max_col)
            #     # チップ初期位置リセット
            #     self.EXExChipPosReset()
            #     # リスト内チップ、フルカスタム以外選択
            #     fileArray = chipArray.copy() #浅いコピー
            #     fileArray.append("_chip_fullcustum.png")
            #     self.EXExChipSelectOther(fileArray, 4)
            #     #OK
            #     self.EXExChipSelOK()
            #     # チップ実行
            #     self.EXExChipExecute(True, 3)
            # #いずれも該当なければPA、フルカスタム以外のチップを選択してOK
            # else:
            #     self.EXExPrint(
            #         self.EXExGetVictoryDefeatPlayer(winner_flag) 
            #             + "ＰＡ／フルカスタム以外選択開始"
            #         , debug_flag=True
            #     )
            #     # リスト内チップ以外選択
            #     self.EXExChipSelectOther(chipArray, 5)
            #     #OK
            #     self.EXExChipSelOK()
            #     # チップ実行
            #     self.EXExChipExecute(True, 2)

    """
    --------------------------------------------------------------------------------------
    プレイヤー共通処理
    --------------------------------------------------------------------------------------
    """
    #プレイヤー共通処理
    # 引数１：プレイヤー区分
    def EXExCustomScreenCommonLogic(self, winner_flag):
        '''
        【概要】
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        if self.init_flag:  #★おそらくバグなので修正用
            self.EXExPrint(
                self.EXExGetVictoryDefeatPlayer(winner_flag) 
                    + "バトルオペレーション スタート！"
            )

    """
    --------------------------------------------------------------------------------------
    対人戦ドロー処理（タイムアウト）
    --------------------------------------------------------------------------------------
    """
    # 対人戦ドロー処理（タイムアウト）
    def EXExPvpResultDraw(self, winner_flag):
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
    def EXExPvpResultToNetWorkMenu(self, winner_flag):
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

# ###################################################################################################################
    """
    --------------------------------------------------------------------------------------
    サンプルメソッド
    --------------------------------------------------------------------------------------
    """
    def sampleMethod(self, testMsg, testInt):
        '''
        【前提】前提条件を書きます
        【戻り値】戻り値の方や日本語の説明を書く
            True:ｘｘｘｘｘ
            False:ｙｙｙｙｙ

        Parameters
        ----------
        testMsg : str
        testInt : int
            受け取った値をメッセージ出力する
        '''
        print(testMsg + ":", testInt)

    """
    --------------------------------------------------------------------------------------
    getter:self._regularChip_used_flag
    --------------------------------------------------------------------------------------
    """
    @property
    def regularChip_used_flag(self):
        return self._regularChip_used_flag 

    """
    --------------------------------------------------------------------------------------
    setter:self._regularChip_used_flag
    --------------------------------------------------------------------------------------
    """
    @regularChip_used_flag.setter
    def regularChip_used_flag(self, flag):
        self._regularChip_used_flag = flag
   
    """
    --------------------------------------------------------------------------------------
    getter:self._pvpBattle_count_max
    --------------------------------------------------------------------------------------
    """
    @property
    def pvpBattle_count_max(self):
        return self._pvpBattle_count_max 

    """
    --------------------------------------------------------------------------------------
    setter:self._pvpBattle_count_max
    --------------------------------------------------------------------------------------
    """
    # 対人戦バトル回数設定
    # 引数１：バトル回数
    @pvpBattle_count_max.setter
    def pvpBattle_count_max(self, count):
        self._pvpBattle_count_max = count

    """
    --------------------------------------------------------------------------------------
    タグ取得
    --------------------------------------------------------------------------------------
    """
    # タグ取得
    # 引数１：ナンバリング
    # 戻り値：[EXEx] ※x=ナンバリング
    def EXExGetSeriesTag(self, series):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        return "[EXE" + series +"]"

    """
    --------------------------------------------------------------------------------------
    メッセージ出力
    --------------------------------------------------------------------------------------
    """
    @abstractmethod
    def EXExPrint(self, series, msg, line_flag=False, debug_flag=False):
        '''
        【前提】前提条件を書きます
        【戻り値】なし

        Parameters
        ----------
        series     : ロックマンエグゼシリーズＮｏ
        msg        : 出力したいメッセージ
        line_flag  : LINE出力有無
        debug_flag : デバッグタグ付与有無

        '''
        if debug_flag :
            addTag = "[debug]"
        else :
            addTag = ""
        outMSG = addTag + msg
        print(self.EXExGetSeriesTag(series) + outMSG)
        if line_flag :
            self.LINE_image(self.EXExGetSeriesTag(series) + outMSG)
   
    """
    --------------------------------------------------------------------------------------
    Templateパス取得
    --------------------------------------------------------------------------------------
    """
    # Templateパス取得
    # 引数１：画像ファイルが格納されているフォルダ
    # 引数２：画像ファイル名
    # 戻り値：foder＋"\"＋file ※例）EXE2\_test.png
    @abstractmethod
    def EXExGetTemplPass(self, foder, file):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        return str(foder + "\\" + file)

    """
    --------------------------------------------------------------------------------------
    プレイヤー区分判定
    --------------------------------------------------------------------------------------
    """
    # プレイヤー区分判定
    # 引数１：True：勝者　False：敗者
    # 戻り値：勝者 敗者
    def EXExGetVictoryDefeatPlayer(self, winner_flag):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        if winner_flag:
            return "[勝者]"
        else:
            return "[敗者]"

    """
    --------------------------------------------------------------------------------------
    チップ初期位置リセット
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ初期位置リセット
    def EXExChipPosReset(self):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        self.press(Button.PLUS, wait=0.1)
        self.press(Hat.LEFT, wait=0.1)
        self.press(Hat.LEFT, wait=0.1)
        self.press(Hat.LEFT, wait=0.1)
        self.press(Hat.LEFT, wait=0.1)
        self.press(Hat.LEFT, wait=0.1)
    
    """
    --------------------------------------------------------------------------------------
    チップ選択処理（行列数指定）
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ選択処理（行列数指定）
    # 引数１：カスタム画面の対象行位置
    # 引数２：カスタム画面の対象列位置
    # 引数３：カスタム画面の最大列数
    def EXExChipSelect(self, row, col, max_col):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        #チップ下移動
        for r in range(0, row):
            self.press(Hat.BTM, wait=0.1)
        #チップ右移動
        if row % 2 == 0:
            for c in range(0, col):
                self.press(Hat.RIGHT, wait=0.1)
        else:
            for c in range(0, max_col - col - 1):
                self.press(Hat.RIGHT, wait=0.1)
        #チップ選択
        self.press(Button.A, wait=0.5)
   
    """
    --------------------------------------------------------------------------------------
    チップ選択確定処理
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ選択確定処理
    def EXExChipSelOK(self):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        self.press(Button.PLUS, wait=0.1)
        self.press(Button.A, wait=0.5)

    """
    --------------------------------------------------------------------------------------
    チップ探索処理
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ探索処理
    # 前提：チップ初期位置リセットをしていること
    # 引数１：認識したい画像ファイル名
    # 戻り値：[探索結果，見つかった行数，見つかった列数]
    def EXExChipTargetSearch(self, file):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        # 補足：移動イメージ
        # →→→→→
        #     ↓
        # ←←←←←
        # Templateパス取得
        templatePass = self.EXExGetTemplPass(file)
        for r in range(0, self.max_row):
            for c in range(0, self.max_col):
                # 画像判定（templatePass）
                if self.isContainTemplate(templatePass, threshold=0.9):
                    # チップ有無フラグ、行列数を設定
                     return [True, r , c]
                # チップ横移動
                if not c == self.max_col - 1:
                    if r % 2 == 0:
                        self.press(Hat.RIGHT, wait=0.1)
                    else:
                        self.press(Hat.LEFT, wait=0.1)
            # チップ下移動
            self.press(Hat.BTM, wait=0.1)
        return [False, -1 , -1]

 
    """
    --------------------------------------------------------------------------------------
    チップ選択処理（指定チップ以外）
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ選択処理（指定チップ以外）
    # 補足：指定された画像以外のチップを指定枚数分選択する
    # 引数１：認識対象チップ画像ファイル名のリスト
    # 引数２：チップ選択枚数
    # 戻り値：True＝指定枚数分チップ選択成功　False=指定枚数分チップ選択失敗
    def EXExChipSelectOther(self, fileArray, select_Max):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        # 補足：移動イメージ
        # →→→→→
        #     ↓
        # ←←←←←
        # ファイル名からパスに変換
        templatePassArray = fileArray.copy()   #浅いコピー
        for f in range(0, len(fileArray)) :
            # Templateパス取得
            templatePassArray[f] = self.EXExGetTemplPass(fileArray[f])
        # チップ選択枚数カウンタ初期化
        select_count = 0
        # チップ移動、選択処理
        for r in range(0, self.max_row):
            for c in range(0, self.max_col):
                # 指定枚数分選択したら終了
                if select_count >= select_Max :
                    return True
                # 画像判定（templatePassArray[?]）
                templatePass_flag = False
                for t in range(0, len(templatePassArray)) :
                    # print("[degug][chip]pass=" + templatePassArray[t]
                            # + ",ArrayCnt=" + str(len(templatePassArray))
                            # + ",r=" + str(r) + ",c=" + str(c) )
                    if self.isContainTemplate(templatePassArray[t], threshold=0.9):
                        templatePass_flag = True
                        # print("[degug][chip]↑検知しました↑")
                        break
                # 指定した画像ではなかった場合
                if not templatePass_flag :
                    # チップ選択
                    self.press(Button.A, wait=0.5)
                    select_count += 1
                    # print("[degug][chip]select_count：" + str(select_count) )
                # チップ横移動
                if not c == self.max_col - 1:
                    if r % 2 == 0:
                        self.press(Hat.RIGHT, wait=0.1)
                        # print("[degug][chip]チップ右移動")
                    else:
                        self.press(Hat.LEFT, wait=0.1)
                        # print("[degug][chip]チップ左移動")
            # チップ下移動
            self.press(Hat.BTM, wait=0.1)
        # 指定枚数分チップ選択ができなかった
        return False
    
    """
    --------------------------------------------------------------------------------------
    チップ実行処理
    前提：ｘｘｘｘ
    対応シリーズ：2,
    --------------------------------------------------------------------------------------
    """
    # チップ実行処理
    # 引数１：チップ実行可否フラグ
    # 引数２：処理開始待ち時間
    def EXExChipExecute(self, chipExe_flag, wait_time):
        '''
        【前提】＠ｄｓｄｄｄ＠
        【戻り値】～～～～

        Parameters
        ----------
        xxx : zzzz
        '''
        # カスタムゲージを画像認識するのはできなかったので別の方策を検討
        # templatePass = "EXE2\_battlescreen_littlegage.png"
        # if self.isContainTemplate(templatePass, threshold=0.9):
        
        #処理開始待ち
        self.wait(wait_time)

        ###使えるかわからないので没になるかも　ここから###
        # Templateパス取得
        templatePass = self.EXExGetTemplPass("_battlefiled_condition_onthetop.png")
        #バトルフィールド状態チェック（ロックマンが上のマスにいる）
        if self.isContainTemplate(templatePass, threshold=0.95):
            #ロックマンを下へ2回移動（対戦相手の前に移動する）
            self.press(Hat.BTM, wait=0.2)
            self.press(Hat.BTM, wait=0.2)
            self.EXExPrint(
                "バトルフィールド状態チェック処理完了："
                    + templatePass
            )
        ###使えるかわからないので没になるかも　ここまで###
            
        #バトルフィールド状態チェック（目の前にストーンキューブがある）
        # →これはバスターで自然体で壊れるの待つ

        #バスターを撃つ　＜障害物がなければバリアを剥がせる
        self.press(Button.B, wait=0.5)
        if chipExe_flag :
            self.wait(1.5)
            self.press(Button.A, wait=0.5)
        #カスタム画面orリザルト画面になるまでバスター
        while True :
            #バスターを撃つ
            self.press(Button.B, wait=0.01)
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battlescreen_start.png")
            #カスタム画面以外の場合
            if self.isContainTemplate(templatePass, threshold=0.9):
                break
            # Templateパス取得
            templatePass = self.EXExGetTemplPass("_battle_result_winner.png")
            #リザルト画面の場合
            if self.isContainTemplate(templatePass, threshold=0.9):
                break