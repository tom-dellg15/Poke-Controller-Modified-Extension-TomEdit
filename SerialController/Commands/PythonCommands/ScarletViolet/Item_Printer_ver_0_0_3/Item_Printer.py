#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.Keys import Button
import time, cv2, os, re, datetime, glob, json
import numpy as np

charlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class Item_Printer(ImageProcPythonCommand):
    NAME = '【ＳＶ】どうぐプリンター出力制御自動化(ver.0.0.3)'
    TAGS = ['SV', 'Ball']

    def __init__(self, cam):
        super().__init__(cam)

    def sendCommand(self, row: str, wait: float = 0.04):
        self.keys.ser.ser.write((row + '\r\n').encode('utf-8'))
        time.sleep(wait)
        self.checkIfAlive()

    def do(self):

        # 実行環境確認
        self.judgePokeConEdition()        

        self.jprint("--------------------------------------------\n"
                    "SVどうぐプリンター出力制御自動化(ver.0.0.3)\n"
                    "Developed  by.フウ(@dragonite303)\n"
                    "Improved   by.ジュナリ(@junari000)\n"
                    "--------------------------------------------")

        if os.path.isdir(os.path.join(os.path.dirname(__file__), "Item_Printer")):
            try:
                self.setTemplateDir(os.path.dirname(__file__) + '/')
            except:
                pass

        self.th = 0.9
        c=0

        ret = self.set_param()

        try:
            self.loopcnt = int(ret[0])
            self.date1 = re.split('[./ :]', ret[1])
            self.waittime1 = float(ret[2])
            self.Printcnt1 = int(ret[3])
            self.date2flag = ret[4]
            self.date2 = re.split('[./ :]', ret[5])
            self.waittime2 = float(ret[6])
            self.Printcnt2 = int(ret[7])
            self.useflag = ret[8]
            self.debug = ret[9]

            self.theme = None

            self.jprint_overwrite("-------------パラメータ設定結果--------------\n"
                                f"繰り返し回数  : {self.loopcnt}\n"
                                f"日時1         : {ret[1]}\n"
                                f"待機時間1     : {self.waittime1}\n"
                                f"プリント回数1 : {self.Printcnt1}連\n"
                                f"日時2を使う   : {self.date2flag}\n"
                                f"日時2         : {ret[5]}\n"
                                f"待機時間2     : {self.waittime2}\n"
                                f"プリント回数2 : {self.Printcnt2}連\n"
                                f"おまかせ選択  : {self.useflag}\n"
                                f"DEBUG         : {self.debug}\n"
                                "---------------------------------------------")  
        except:
            self.jprint("パラメータが不正です。終了します。")
            self.finish()
        
        for loop in range(self.loopcnt):
            self.jprint(f"{loop+1}回目")
            for ii, (date_sel, waittime_sel, Print_cnt) in enumerate(zip([self.date1, self.date2], [self.waittime1, self.waittime2], [self.Printcnt1, self.Printcnt2])):
                self.target_year = int(date_sel[0])
                self.target_month = int(date_sel[1])
                self.target_day = int(date_sel[2])
                self.target_hour = int(date_sel[3])
                self.target_minute = int(date_sel[4])
                

                # スキップ処理
                if self.Printcnt2==1 and ii==0 and c>0:
                    c+=1
                    if c==10:c=0
                    continue  
                elif self.Printcnt2==5 and ii==0 and c>0:
                    c=0
                    continue         

                if ii == 1 and self.date2flag == False:    
                    pass
                else:
                    # 話しかけて待機する
                    self.press(Button.A, wait=2.0, duration=0.1)
                    self.press(Button.A, wait=1.0, duration=0.1)
                    
                    # HOME画面に移動して日付を変更する
                    self.press(Button.HOME, wait=1.2, duration=0.1)
                    
                    if self.theme == None:
                        self.detectSwitchTheme()
                        self.jprint(f"Switchテーマ:{self.theme}")

                    self.quickDateChange()

                    self.press(Button.HOME, wait=1.2, duration=0.1)
                    self.press(Button.HOME, wait=1.5, duration=0.1)
                    
                    # 待機時間を求める
                    elapsed = time.perf_counter() - self.start_time
                    self.wait_time = waittime_sel - elapsed

                    # 待機
                    if self.wait_time>0:
                        #time.sleep(self.wait_time)  
                        time.sleep(self.wait_time - 1)

                    while (time.perf_counter() - self.start_time) <= waittime_sel:
                        pass                    

                    # どうぐプリンターを開く
                    self.press(Button.A, wait=0.1, duration=0.1)
                    
                    while not self.isContainTemplate('Item_Printer/Button_B.png', threshold=0.8, crop=[1054,671,1270,711], use_gray=True, show_value=False):
                        self.wait(0.1)      
                    self.wait(1.5)  
                
                # 回数処理
                if self.Printcnt1==self.Printcnt2 and c>0:
                    pass
                elif self.Printcnt2==1 and c>1:
                    pass
                else:
                    mode = 0 if self.isContainTemplate('Item_Printer/mark_L.png', threshold=0.8, crop=[1035,240,1081,279], use_gray=True, show_value=False) else 1
                    count_now = self.count_check(mode)
                    if count_now == 1:
                        if Print_cnt == 5:
                            self.press(Button.R, wait=1.0)
                        elif Print_cnt == 10:
                            self.press(Button.L, wait=1.0)
                    elif count_now == 5:
                        if Print_cnt == 10:
                            self.press(Button.R, wait=1.0)
                        elif Print_cnt == 1:
                            self.press(Button.L, wait=1.0)
                    elif count_now == 10:
                        if Print_cnt == 1:
                            self.press(Button.R, wait=1.0)
                        elif Print_cnt == 5:
                            self.press(Button.L, wait=1.0)
                                    
                # おまかせ選択
                if self.useflag:
                    self.press(Button.X, wait=2.0, duration=0.1)
                
                # ガチャを回す
                self.press(Button.A, wait=6.0)       
                self.press(Button.A, wait=0.5)  
                self.press(Button.A, wait=0.5)       
                while not self.isContainTemplate('Item_Printer/Button_A.png', threshold=0.8, crop=[1054,671,1270,711], use_gray=True, show_value=False):
                    self.press(Button.B, wait=0.1)   
                
                if self.debug:
                    #for i in range(10):
                        #self.press(Button.A, wait=0.5)
                    self.wait(0.5)  
                    dt = datetime.datetime.today()
                    self.camera.saveCapture(filename=f'{"".join(date_sel)}_{waittime_sel}_{dt.strftime("%Y%m%d%H%M%S")}')
                
                # ガチャ結果
                self.press(Button.A, wait=0.5) 
                self.press(Button.A, wait=0.5)       
                while not self.isContainTemplate('Item_Printer/Button_B.png', threshold=0.8, crop=[1054,671,1270,711], use_gray=True, show_value=False):
                    self.wait(0.1)
                self.wait(0.5) 
                
                # チャンス状態にはいったかを確認
                if ii == 0 and self.isContainTemplate('Item_Printer/mark_L.png', threshold=0.8, crop=[1035,240,1081,279], use_gray=True, show_value=False):
                    self.press(Button.B, wait=0.2, duration=0.1)
                    self.press(Button.B, wait=6.0, duration=0.1)
                    print("チャンス状態に入りませんでした。リトライします。")
                    break
                
                if ii == 0 and self.date2flag == False:  
                    pass
                else:
                    self.press(Button.B, wait=0.2, duration=0.1)
                    self.press(Button.B, wait=6.0, duration=0.1)
                    if c==0 and ii==0:
                        c=1

                    

    def set_param(self):
        '''
        プリセット機能付きパラメータ設定ダイアログ
        developed by フウ
        '''
        def get_json():
            preset_file_list = glob.glob(os.path.join(os.path.dirname(__file__), "preset", "**", "*.json"), recursive=True)
            
            len_pass = len(os.path.join(os.path.dirname(__file__)))
            preset_name_list = [file[len_pass + 8:-5] for file in preset_file_list]

            return preset_name_list

        def get_setting(name):
            preset_file = os.path.join(os.path.dirname(__file__), "preset", f"{name}.json")
            try:
                with open(preset_file, encoding='utf-8') as f:
                    file = json.load(f)
                    return file
            except:
                return None

        def save_setting(name, setting_dict):
            preset_file = os.path.join(os.path.dirname(__file__), "preset", f"{name}.json")
            with open(preset_file, 'w', encoding='utf-8') as f:
                json.dump(setting_dict, f, indent=4, ensure_ascii=False)

        preset_name_list = get_json()

        skipflag = False
        skipflag2 = False

        while True:

            if not skipflag2:
                # デフォルト値
                loopcnt = "11"
                date1 = "2024.4.16 7:50"
                waittime1 = "6.7"
                printcnt1 = "1"
                date2flag = True
                date2 = "2016.5.20 2:11"
                waittime2 = "11.7"
                printcnt2 = "10"
                useflag = True
                debug = False
    
            if not skipflag:
                # GUI画面表示
                ret = self.dialogue6widget("プリセット選択", [["Combo", "------------------------------プリセット選択------------------------------", preset_name_list, "選択して下さい"]])
                if type(ret) == bool:
                    if ret == False:
                        self.jprint("キャンセルが押されました。プログラムを終了します。")
                        self.finish()
                elif ret[0] == "選択して下さい":
                    self.jprint("プリセットを選択しなかったのでデフォルト値で起動します。")
                else:
                    try:
                        preset = get_setting(ret[0])
                        loopcnt   = preset["loopcnt"]
                        date1     = preset["date1"]
                        waittime1 = preset["waittime1"]
                        printcnt1 = preset["printcnt1"]
                        date2flag = preset["date2flag"]
                        date2     = preset["date2"]
                        waittime2 = preset["waittime2"]
                        printcnt2 = preset["printcnt2"]
                        useflag   = preset["useflag"]
                        debug     = preset["debug"]
                    except:
                        self.jprint("プリセットに問題があります。デフォルト値を設定します。")
                        skipflag = True
                        continue
            
            skipflag = False
            skipflag2 = False                    

            dialogue_list = [
                                ["Entry", "繰り返し回数", loopcnt],
                                ["Entry", "日時1", date1],
                                ["Entry", "待機時間1", waittime1],
                                ["Radio", "プリント回数1", ["1", "5", "10"], printcnt1],
                                ["Check", "日時2を使う", date2flag],
                                ["Entry", "日時2", date2],
                                ["Entry", "待機時間2", waittime2],
                                ["Radio", "プリント回数2", ["1", "5", "10"], printcnt2],
                                ["Check", "おまかせ選択", useflag],
                                ["Check", "DEBUG", debug],
                                ["Entry", "(プリセットを保存する場合のみ)ファイル名", ""],
                            ]

            if self.mode_extension:
                dialogue_list.insert(8, ["Next"])
                dialogue_list.insert(4, ["Next"])

            ret = self.dialogue6widget("どうぐプリンター設定", dialogue_list)

            if type(ret) == bool:
                if ret == False:
                    self.jprint("キャンセルが押されました。プログラムを終了します。")
                    self.finish()
            if ret[-1] == "選択して下さい":
                self.jprint("そのファイル名は使えません。変更してください。")
                skipflag = True
                skipflag2 = True
            elif "" not in ret[:-1]:
                break
            else:
                self.jprint("未設定項目があります。再度設定してください。")

        setting_dict = {
                            'loopcnt'   : ret[0],
                            'date1'     : ret[1],
                            'waittime1' : ret[2],
                            'printcnt1' : ret[3],
                            'date2flag' : ret[4],
                            'date2'     : ret[5],
                            'waittime2' : ret[6],
                            'printcnt2' : ret[7],
                            'useflag'   : ret[8],
                            'debug'     : ret[9],
                        }

        save_setting("前回の設定", setting_dict)
        if ret[10] != "":
            save_setting(ret[10], setting_dict)
        
        return ret

    def detectSwitchTheme(self):
        '''
        Swithテーマ検出
        developed by フウ
        '''
        src = self.camera.readFrame()
        src = src[510:520, 100:110]
        img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        if np.average(img_gray) > 128:
            self.theme = "white"
        else:
            self.theme = "black"
    
    def quickDateChange(self):
        '''
        高速日時変更(指定日時への変更対応版)
        developed by フウ
        '''
        Neutral      = "0x0003 8 80 80 80 80"   # NEUTRAL
        Button_A     = "0x0013 8 80 80 80 80"   # A
        # Home         = "0x4000 8 80 80 80 80"   # HOME
        Lstick_down  = "0x0003 8 80 ff 80 80"   # LSTICK-DOWN
        Rstick_down  = "0x0003 8 80 80 80 ff"   # RSTICK-DOWN
        Lstick_right = "0x0003 8 ff 80 80 80"   # LSTICK-RIGHT
        Rstick_right = "0x0003 8 80 80 ff 80"   # RSTICK-RIGHT
        Lstick_left  = "0x0003 8 00 80 80 80"   # LSTICK-LEFT
        
        # ゲーム選択画面⇒設定
        self.sendCommand(Lstick_left,  wait=0.04) 
        self.sendCommand(Neutral,      wait=0.16) # 設定画面に移動できない場合は要調整。
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Lstick_left,  wait=0.04)
        self.sendCommand(Button_A,     wait=0.80)

        # 設定の一番下まで移動
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Button_A,     wait=0.20)

        # 日付と時刻を選択
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.32) # カーソルが日付と時刻を選択しない場合は要調整。
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Button_A,     wait=0.04) 
        self.sendCommand(Neutral,      wait=0.20) # タイムゾーンを変更してしまう場合はwaitを大きくすること。

        # 現在の日付と時刻を選択
        self.sendCommand(Lstick_down,  wait=0.04)
        self.sendCommand(Rstick_down,  wait=0.04)
        self.sendCommand(Button_A,     wait=0.20) # 時刻変更でminを変更しない場合はwaitを大きくすること。

        self.wait(0.5)
        while True:
            date_upper = self.check_datetime_wo_ocr(0, th=self.th)
            date_lower = self.check_datetime_wo_ocr(1, th=self.th)
            date = date_upper + date_lower
            if len(date) == 12:
                break
            else:
                self.th = self.th - 0.01

        # self.jprint(date)
        year_now = int(date[0:4])
        month_now = int(date[4:6])
        day_now = int(date[6:8])
        hour_now = int(date[8:10])
        min_now = int(date[10:12])

        
        year_offset = self.target_year - year_now

        # 以下、単純化できるはずなんだけど...
        month_offset = self.target_month - month_now
        if month_offset > 6:
            month_offset = month_offset - 12
        elif month_offset < -6:
            month_offset = month_offset + 12

        day_offset = self.target_day - day_now  # 考えるの面倒
        if self.target_month in [1, 3, 5, 7, 8, 10, 12]:
            a = [15, 31]
        elif self.target_month in [4, 6, 9, 11]:
            a = [15, 30]
        else:
            a = [14, 28] if self.target_year % 4 != 0 else [14, 29]
        if day_offset > a[0]:
            day_offset = day_offset - a[1]
        elif day_offset < -a[0]:
            day_offset = day_offset + a[1]
        
        hour_offset = self.target_hour - hour_now
        if hour_offset > 12:
            hour_offset = hour_offset - 24
        elif hour_offset < -12:
            hour_offset = hour_offset + 24

        min_offset = self.target_minute - min_now
        if min_offset > 30:
            min_offset = min_offset - 60
        elif min_offset < -30:
            min_offset = min_offset + 60
        # self.jprint(f"{month_offset},{day_offset},{hour_offset},{min_offset}")

        # 時間変更画面
        self.change_value(year_offset)
        self.sendCommand(Lstick_right, wait=0.04)
        self.change_value(month_offset)
        self.sendCommand(Rstick_right, wait=0.04)
        self.change_value(day_offset)
        self.sendCommand(Lstick_right, wait=0.04)
        self.change_value(hour_offset)
        self.sendCommand(Rstick_right, wait=0.04)
        self.change_value(min_offset)
        self.sendCommand(Lstick_right, wait=0.04)
        
        self.start_time = time.perf_counter()   # できるだけAを押すタイミング
        self.sendCommand(Button_A,     wait=0.0)
        
        time.sleep(0.04)
        
        self.sendCommand(Neutral,      wait=0.10) # HOME画面に戻らない場合は要調整。

        # # ホーム画面に戻る
        # self.sendCommand(Home,         wait=0.08)
        # self.sendCommand(Neutral,      wait=0.10)
    
    def change_value(self, cnt):
        '''
        高速日時変更(数値変更部分)
        developed by フウ
        '''
        Lstick_up    = "0x0003 8 80 00 80 80"   # LSTICK-DOWN
        Rstick_up    = "0x0003 8 80 80 80 00"   # RSTICK-DOWN
        Lstick_down  = "0x0003 8 80 ff 80 80"   # LSTICK-DOWN
        Rstick_down  = "0x0003 8 80 80 80 ff"   # RSTICK-DOWN
        if cnt == 0:
            pass
        elif cnt > 0:
            for i in range(cnt):
                if i % 2 == 0:
                    self.sendCommand(Lstick_up, wait=0.04)
                else:
                    self.sendCommand(Rstick_up, wait=0.04)
        else:
            for i in range(-cnt):
                if i % 2 == 0:
                    self.sendCommand(Lstick_down, wait=0.04)
                else:
                    self.sendCommand(Rstick_down, wait=0.04)
        return

    def check_datetime_wo_ocr(self, num, th=0.9):
        '''
        日時検出(流用)
        developed by フウ
        '''
        src = self.camera.readFrame()
        if num == 0:
            src = src[437:500, 182:336]
        else:
            src = src[437:500, 336:887]
        img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        
        box = []
        for test in charlist:
            if self.mode_extension:
                char_file_name = ImageProcPythonCommand.template_path_name + f'Item_Printer/Character/{test}_{num}_{self.theme}.png'                
            else:
                char_file_name = f'./Template/Item_Printer/Character/{test}_{num}_{self.theme}.png'                
            if os.path.exists(char_file_name):
                template = cv2.imread(char_file_name)
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                # 処理対象画像に対して、テンプレート画像との類似度を算出する
                res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                # 類似度の高い部分を検出する
                threshold = th
                loc = np.where(res >= threshold)
                max_val = np.max(res)
                try:
                    loc_sorted = sorted(loc[1])
                    box.append([loc_sorted[0], test, max_val])
                    box_temp = [loc_sorted[0]]
                    for i in loc_sorted[1:]:
                        for j in box_temp:
                            if abs(i-j) > 5:
                                box.append([i, test, max_val])
                                box_temp=[i]
                except:
                    pass
            else:
                pass
        box.sort(key=lambda x: x[0])
        text = ""
        for i in box:
            flag = True
            for j in box:
                if abs(i[0] - j [0]) < 5 and i != j:
                    if i[2] < j [2]:
                        flag = False
            if flag:
                text = text + i[1]
        return text


    def count_check(self, mode: int=0):
        '''
        現在のプリント回数を取得する(w/o画像認識)
        developed by フウ
        '''
        left_pos_list = []

        for _ in range(3):
            left_pos_list.append(self.left_pos_check(mode))
            self.press(Button.R, wait=0.3)

        if np.argmin(left_pos_list) == 0:
            return 10
        elif np.argmin(left_pos_list) == 1:
            return 5
        else:
            return 1

    def left_pos_check(self, mode: int):
        '''
        白い部分のうち最も左の部分のx座標を取得
        developed by フウ
        '''
        src = self.camera.readFrame()

        if mode == 0:
            src = src[243:279, 1080:1175]
        else:
            src = src[305:341, 1080:1175]
        
        img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, img_bw = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)

        pos_left = np.shape(img_bw)[1]
        for i in range(np.shape(img_bw)[0]):
            for j in range(np.shape(img_bw)[1]):
                if img_bw[i,j] != 0 and j < pos_left:
                    pos_left = j

        return pos_left    
    
    def judgePokeConEdition(self):
        '''
        PokeCon判別プログラム改
        developed by 非公表
        '''        
        if hasattr(self.__class__, 'print_t2b'):    # 継承している関数にprint_t1b関数が含まれるか? print_tb1関数はextension版のみ。
            self.mode_extension = True
            self.jprint("実行環境:Poke-Controller-Modified Extension")
        elif hasattr(self.__class__, 'dialogue6widget'):   # 継承している関数にdialogue6widget関数が含まれるか? dialogue6widget関数はmodified版/extension版のみ。
            self.mode_extension = False
            self.jprint("実行環境:Poke-Controller-Modified")
        else:
            print("本家PokeConでは実行できません。")
            self.finish()

    def jprint(self, text: str):
        '''
        print出力(上書きなし)
        developed by 非公表
        '''
        if self.mode_extension:
            self.print_tbs("a", text + "\n")
        else:
            print(text)

    def jprint_overwrite(self, text: str):
        '''
        print出力(上書きあり)
        developed by 非公表
        '''
        if self.mode_extension:
            self.print_tb("w", text + "\n")
        else:
            print(text)
