#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import threading
from abc import abstractclassmethod
from time import sleep
import random
import time
from logging import getLogger, DEBUG, NullHandler

from LineNotify import Line_Notify
from . import CommandBase
from .Keys import Button, Direction, KeyPress
from .PythonCommandBase import ImageProcPythonCommand

import numpy as np


# Python command
TEMPLATE_PATH = "./Template/"

class ImageProcPythonCommandTrim(ImageProcPythonCommand):

    '''
    --------------------------------------------------------------------------------------
     画像認識コマンド拡張版 v1.0 Release.2023/1/2
     Copyright(c) 2023 mikan kato

     ・１/14 コメント整備
     ・メソッド名誤字修正　誤）isContainTemplatPositionBGR
    --------------------------------------------------------------------------------------
     ・isContainTemplateメソッド
        一致画像の有無を返す
        【機　能】座標によるマッチング範囲指定・二値化マッチング・マスク機能
        【戻り値】bool値

     ・isContainTemplatePositionメソッド
        一致画像の左上の座標を返す
        【機　能】座標によるマッチング範囲指定・二値化マッチング・マスク機能
        【戻り値】一致あり：配列　[int(left),int(top)]
                 一致無し：Mone

     ・isContainTemplatePositionBGRメソッド
        指定色域で一致した範囲の左上の座標を返す
        【機　能】座標によるマッチング範囲指定・RGBによる指定色域でのマッチング・マスク機能
        【戻り値】一致あり：配列　[int(left),int(top)]
                 一致無し：None
        ※HSBよりRGBの方が各自調整しやすいかと思い採用しています
    --------------------------------------------------------------------------------------
    '''
    # Judge if current screenshot contains an image using template matching
    # It's recommended that you use gray_scale option unless the template color wouldn't be cared for performace
    # 現在のスクリーンショットと指定した画像のテンプレートマッチングを行います
    # 色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します
    def isContainTemplate(self, template_path, threshold=0.7, use_gray=True, show_value=False, show_position=True, show_only_true_rect=True, ms=2000,
                          area=None,use_binary=False,threshold_binary=128,mask_path=None):
        """ 
        一致画像の有無を返す
        【機　能】座標によるマッチング範囲指定・二値化マッチング・マスク機能
        【戻り値】bool値

        Parameters
        ----------
        area : [int,int,int,int]
            範囲指定をする際に使用
            top,bottom,left,rightで記述
        use_binary : bool
            二値化する際に使用
            使用時はTrueにする
        threshold_binary : int
            二値化の閾値を設定する際に使用
            0～255の値を指定する
        mask_path : string
            マスクを設定する際に使用
            別途用意したマスク画像をtemplateフォルダに格納して、パスを記載する
        """
        src = self.camera.readFrame()
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src

        # areaに値があればトリミングする[top:bottom,left:right] 
        src = src[area[0]:area[1], area[2]:area[3]] if area is not None else src        
        # mask_pathに値があれば、画像にマスクを設定する（マスク画像の黒い部分が塗りつぶされる）
        if mask_path is not None:
            mask = cv2.imread(TEMPLATE_PATH + mask_path, cv2.IMREAD_GRAYSCALE)
            src = cv2.bitwise_and(src, mask)

        template = cv2.imread(TEMPLATE_PATH + template_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
        w, h = template.shape[1], template.shape[0]

        # 二値化フラグがTrueなら画像を二値化する
        if use_binary:
            _, src = cv2.threshold(src, threshold_binary, 255, cv2.THRESH_BINARY) 
            _, template = cv2.threshold(template, threshold_binary, 255, cv2.THRESH_BINARY)

        # デバッグ用の画像出力処理（不要ならコメントアウトする）
        cv2.imwrite(TEMPLATE_PATH + 'debug_template.png', template)
        cv2.imwrite(TEMPLATE_PATH + 'debug_src.png', src)
        
        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(src, template, method)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if show_value:
            print(template_path + ' ZNCC value: ' + str(max_val))

        top_left = max_loc
        if area is not None:
            top_left = (top_left[0] + area[2], top_left[1] + area[0])
        bottom_right = (top_left[0] + w + 1, top_left[1] + h + 1)
        tag = str(time.perf_counter()) + str(random.random())
        if max_val >= threshold:
            if self.gui is not None and show_position:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='blue',
                                 tag=tag,
                                 ms=ms)
            return True
        else:
            if self.gui is not None and show_position and not show_only_true_rect:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='red',
                                 tag=tag,
                                 ms=ms)
            return False

    def isContainTemplatePosition(self, template_path, threshold=0.7, use_gray=True, show_value=False, show_position=True, show_only_true_rect=True, ms=2000,
                          area=None, use_binary=False, threshold_binary=128, mask_path=None):
        """ 
        一致画像の左上の座標を返す
        【機　能】座標によるマッチング範囲指定・二値化マッチング・マスク機能
        【戻り値】一致あり：配列　[int(left),int(top)]
                 一致無し：Mone

        Parameters
        ----------
        area : [int,int,int,int]
            範囲指定をする際に使用
            top,bottom,left,rightで記述
        use_binary : bool
            二値化する際に使用
            使用時はTrueにする
        threshold_binary : int
            二値化の閾値を設定する際に使用
            0～255の値を指定する
        mask_path : string
            マスクを設定する際に使用
            別途用意したマスク画像をtemplateフォルダに格納して、パスを記載する
        """
        src = self.camera.readFrame()
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src

        # areaに値があればトリミングする[top:bottom,left:right] 
        src = src[area[0]:area[1], area[2]:area[3]] if area is not None else src        
        # mask_pathに値があれば、画像にマスクを設定する（マスク画像の黒い部分が塗りつぶされる）
        if mask_path is not None:
            mask = cv2.imread(TEMPLATE_PATH + mask_path, cv2.IMREAD_GRAYSCALE)
            src = cv2.bitwise_and(src, mask)

        template = cv2.imread(TEMPLATE_PATH + template_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
        w, h = template.shape[1], template.shape[0]

        # 二値化フラグがTrueなら画像を二値化する
        if use_binary:
            _, src = cv2.threshold(src, threshold_binary, 255, cv2.THRESH_BINARY) 
            _, template = cv2.threshold(template, threshold_binary, 255, cv2.THRESH_BINARY)

        # デバッグ用の画像出力処理（不要ならコメントアウトする）
        cv2.imwrite(TEMPLATE_PATH + 'debug_template.png', template)
        cv2.imwrite(TEMPLATE_PATH + 'debug_src.png', src)

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(src, template, method)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if show_value:
            print(template_path + ' ZNCC value: ' + str(max_val))
            
        top_left = max_loc
        if area is not None:
            top_left = (top_left[0] + area[2], top_left[1] + area[0])
        bottom_right = (top_left[0] + w + 1, top_left[1] + h + 1)
        tag = str(time.perf_counter()) + str(random.random())
        if max_val >= threshold:
            if self.gui is not None and show_position:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='blue',
                                 tag=tag,
                                 ms=ms)
            return top_left
        else:
            if self.gui is not None and show_position and not show_only_true_rect:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='red',
                                 tag=tag,
                                 ms=ms)
            return None

    def isContainTemplatePositionBGR(self, template_path, threshold=0.7, show_value=False, show_position=True, show_only_true_rect=True, ms=2000,
                          area=None, lower=None, upper=None, mask_path=None):
        """ 
        指定色域で一致した範囲の左上の座標を返す
        【機　能】座標によるマッチング範囲指定・RGBによる指定色域でのマッチング・マスク機能
        【戻り値】一致あり：配列　[int(left),int(top)]
                 一致無し：None

        Parameters
        ----------
        area : [int,int,int,int]
            範囲指定をする際に使用
            top,bottom,left,rightで記述
        lower : [int,int,int]
            BGRの下限値を設定（0～255）
        upper : [int,int,int]
            BGRの上限値を設定（0～255）
        mask_path : string
            マスクを設定する際に使用
            別途用意したマスク画像をtemplateフォルダに格納して、パスを記載する
        """
        # 抽出する色の上下限を設定する（BGR）
        lower_array = np.array(lower)          # 下限
        upper_array = np.array(upper)          # 上限

        src = self.camera.readFrame()
        # areaに値があればトリミングする[top:bottom,left:right] 
        src = src[area[0]:area[1], area[2]:area[3]] if area is not None else src

        # 画像を変換する
        src = cv2.inRange(src, lower_array, upper_array)  # inRangeで元画像を２値化

        # mask_pathに値があれば、画像にマスクを設定する（マスク画像の黒い部分が塗りつぶされる）
        if mask_path is not None:
            mask = cv2.imread(TEMPLATE_PATH + mask_path, cv2.IMREAD_GRAYSCALE) 
            src = cv2.bitwise_and(src, mask)

        # 画像を変換する
        template = cv2.imread(TEMPLATE_PATH + template_path)
        template = cv2.inRange(template, lower_array, upper_array)  # inRangeで元画像を２値化

        w, h = template.shape[1], template.shape[0]

        # デバッグ用の画像出力処理（不要ならコメントアウトする）
        cv2.imwrite(TEMPLATE_PATH + 'debug_template.png', template) 
        cv2.imwrite(TEMPLATE_PATH + 'debug_src.png', src)

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(src, template, method)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if show_value:
            print(template_path + ' ZNCC value: ' + str(max_val))
            
        top_left = max_loc
        bottom_right = (top_left[0] + w + 1, top_left[1] + h + 1)
        tag = str(time.perf_counter()) + str(random.random())
        if max_val >= threshold:
            if self.gui is not None and show_position:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='blue',
                                 tag=tag,
                                 ms=ms)
            return top_left
        else:
            if self.gui is not None and show_position and not show_only_true_rect:
                # self.gui.delete("ImageRecRect")
                self.gui.ImgRect(*top_left,
                                 *bottom_right,
                                 outline='red',
                                 tag=tag,
                                 ms=ms)
            return None
            