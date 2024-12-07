#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick
import pyaudio
import cv2
import time
import numpy as np
from scipy import signal
from scipy import fftpack
from scipy.io.wavfile import read
from scipy.io.wavfile import write
#from scipy import spatial
#バージョン記載変更
version = '1.0'

class SpctPeak(ImageProcPythonCommand):
	NAME = 'SoundTest_音声録音(8秒)' + version
	
	def __init__(self, cam):
		super().__init__(cam)
		#----------------------------------
		'''
		6秒間、音声を録音して終了します
		マイクなど他に音が鳴る入力機器を接続していない状態で実行してください
		'''
		#----------------------------------
		self.recdata = []
		self.compdata = []
	#print('プログラム更新完了_prog:scpt')
	
	def do(self):
		self.audioRec(8)	#8秒間録音(引数で録音時間(秒)を変更可能)
		self.finish()
	
	def audioRec(self, time):
		RATE = 8000			#サンプリングレート
		framesize = 1024	#フレームサイズ
		input_idx = 0		#マイクのチャンネル
		rectime = time		#録音時間(秒)
		
		pa = pyaudio.PyAudio()
		data = []
		dt = 1 / RATE			#1サンプルの秒数
		print('----------録音開始--------')
		#ストリームの開始
		stream = pa.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, input_device_index=input_idx, frames_per_buffer=framesize)
		#フレームサイズ毎に音声を録音
		for i in range(int(((rectime * RATE) / framesize))):
			frame = stream.read(framesize)	#録音を読み取る部分
			data.append(frame)				#入れ物に格納する部分
		#ストリームの終了
		stream.stop_stream()	#然るべき回数繰り返された後は終了。
		print('----------録音終了--------')
		stream.close()
		pa.terminate()
		#フレームごとのデータをまとめる処理
		data = b''.join(data)
		#データをNumpy配列に変換
		data = np.frombuffer(data, dtype='int16')
		#書き出し
		write('Template/CompSx/recdata.wav', RATE, data)
		return data
	
