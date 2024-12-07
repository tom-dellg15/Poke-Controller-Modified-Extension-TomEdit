#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Hat, Button, Direction, Stick
from scipy import signal
from scipy.io.wavfile import write
import pyaudio
import numpy as np
import time
import os
import os.path
import pathlib
import wave
#バージョン記載変更
version = '1.0'

class FieldSpct(ImageProcPythonCommand):
	NAME = 'SoundTest_音声比較_v' + version
	
	def __init__(self, cam):
		super().__init__(cam)
		self.starts = 0			#音声認識処理内の時間計測用
		self.ends = 0			#音声認識処理内の時間計測用
		#----------------------------------
		'''
		
		＜前提条件＞
		PyAudioのインストールが必要です
		
		＜事前準備＞
		比較する音声データを「hikaku.wav」というファイル名で用意する必要があります
		また、「hikaku.wav」を使用するようにプログラムの修正が必要です
		詳細な使い方は下記の記事を参照ください
		https://note.com/ru_no_gu/n/n4a266785dbe9
		'''
		#----------------------------------
		
		
	
	def do(self):
		'''
		#必要な前処理を入力
		'''
		
		#音声認識処理
		self.audiosx()
		
		'''
		#必要な後処理を入力
		'''
		self.finish()
	
	#音声認識
	def audiosx(self):
		CHUNK = 16384	#事前に用意した音声データの再生時間の2倍以上かつ、2のべき乗の値(1秒以下ならこれで大丈夫なはず)
		global RATE
		RATE = 8000		#事前に用意した音声データと同じサンプリングレート
		dt = 1/RATE
		freq = np.linspace(0,1.0/dt,CHUNK)
		fn = 1/dt/2;    #ナイキスト周波数
		detect_high = False
		FORMAT   = pyaudio.paInt16
		CHANNELS = 1	#モノラル
		global freqs2, times2, Sx2
		self.starts = time.time()
		dummycount = 0
		
		#取得した音声を扱う関数(★checkIfAlive()の判定を削除すると、Poke-Controllerで「stop」を押しても止まらなくなるので注意)
		def callback(in_data, frame_count, time_info, status):
			#print('Sx2:',Sx2)
			self.ends = time.time()
			ndarray = np.frombuffer(in_data, dtype='int16')
			#print('nd',ndarray)
			#今回取得した音声と、前回取得した音声の後ろ半分を結合する(初回のみ前回データがないのでelse)
			if 'ndarraybk' in locals():
				recdata = np.append(ndarraybk, ndarray)
			else:
				recdata = ndarray[:]
			#print('rc',recdata)
			N=1024
			#スペクトログラム作成：freqsはサンプル周波数の配列、timesはサンプル時間の配列、Sxはスペクトログラム
			freqs1, times1, Sx1 = signal.spectrogram(recdata, fs=RATE, window='hanning',
													nperseg=N, noverlap=N-100, 
													detrend=False, scaling='spectrum')
			#print('Sx1:',Sx1)
			#print('Sx1',Sx1.shape)
			#print('Sx2',Sx2.shape)
			#低周波数帯域をカット(780Hzくらいまでをカット(RATE = 8000の場合))
			Sx1[:100] = 0
			#取得した音声と用意した音声のコサイン類似度比較
			maxi, maxv = cosSim(Sx1, Sx2)
			print('一致率:', round(maxv, 3))
			
			#閾値以上の場合に一致したと検知(今回は0.8)
			if maxv > 0.8:
				print('---------------------音声を検知！----------------------')
				myh = str(int(((self.ends - self.starts) / 3600) % 24))
				mym = str(int(((self.ends - self.starts) / 60) % 60))
				mys = str(int((self.ends - self.starts) % 60))
				print('経過時間' + myh + '時間' + mym + '分' + mys + '秒')
				self.press(Button.CAPTURE, 1.0, 1.0)
				self.press(Button.HOME, 0.3, 0.3)
				self.finish()
			
			#スライシングで値渡し
			ndarraybk = ndarray[:]
			
			#Poke-Controller側で「stop」ボタンが押された際にcallback関数を終了する処理
			if not self.checkIfAlive():
				stream.stop_stream()
				stream.close()
			
			'''
			##取得した音声の出力(デバッグ用)
			#フレームごとのデータをまとめる処理
			recdata = b"".join(recdata)
			#データをNumpy配列に変換
			recdata = np.frombuffer(recdata, dtype="int16")
			filename = 'recdata' + str(self.ends - self.starts) + '.wav'
			#書き出し
			write(filename, RATE, recdata)
			'''
			
			return (None, pyaudio.paContinue)
			
		
		#事前に用意した音声データからスペクトログラムを作成する関数
		def wavsignal(filename):
			wav = wave.open(filename, "r")
			#フレーム数
			nframes = wav.getnframes()
			#サンプリング周波数
			framerate = wav.getframerate()
			#print(framerate)
			mydata = wav.readframes(nframes)
			mydata = np.frombuffer(mydata, dtype="int16")
			wav.close()
			N=1024
			#スペクトログラム作成：freqsはサンプル周波数の配列、timesはサンプル時間の配列、Sxはスペクトログラム
			freqs, times, Sx = signal.spectrogram(mydata, fs=framerate, window='hanning',
													nperseg=N, noverlap=N-100, 
													detrend=False, scaling='spectrum')
			#print("freqs",freqs.shape,freqs)
			#print("times",times.shape,times)
			#print("Sx",Sx.shape,Sx)
			return freqs, times, Sx
		
		#2つのスペクトログラムのコサイン類似度を比較する関数(引数1が今回取得した音声データ、引数2が事前に用意した音声データ)
		def cosSim(recSx, compSx):
			#配列を転置
			recSxt = recSx.T
			compSxt = compSx.T
			compSxtf = compSxt.flatten()
			maxi = 0
			maxv = 0
			#類似度確認
			for i in range(len(recSxt)-len(compSxt)+1):
				recSxtc = recSxt[i:i+len(compSxt)]
				#print(Sx1tc.shape)
				#1次元化
				recSxtcf = recSxtc.flatten()
				#print(len(Sx1tcf))
				#コサイン類似度
				my_cos_sim = np.dot(recSxtcf, compSxtf)/(np.linalg.norm(recSxtcf)*np.linalg.norm(compSxtf))
				if maxv < my_cos_sim:
					maxv = my_cos_sim
					maxi = i
				#print(i,', cos_sim:',my_cos_sim)
			return maxi, maxv
		
		'''
		#事前に用意した音声データの比較は①音声データのwav, ②スペクトログラムのcsvのどちらかを選択する
		'''
		#①事前に用意した音声データを読み込む処理
		#freqs2, times2, Sx2 = wavsignal('Template/CompSx/hikaku.wav')
		#②または事前にcsv変換したスペクトログラムを読み込む処理
		Sx2 = np.loadtxt('Template/CompSx/hikaku.csv', delimiter=',', dtype='float32')
		#低周波数帯域をカット(780Hzくらいまでをカット(RATE = 8000の場合))
		Sx2[:100] = 0
		print(Sx2.shape)
		
		global stream
		P = pyaudio.PyAudio()
		stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE,
			 frames_per_buffer=CHUNK, input=True, output=False,
			 stream_callback=callback
			 )
		stream.start_stream()
		
		while stream.is_active():
			try:
				dummycount+=1	#デバッグ用の無駄な処理、プログラム流用時は不要なので削除する
				
				'''
				#音声認識処理中に実施したい処理を記載する
				'''
				
				#音声認識処理を終了(try内を無限ループさせたくない場合はコメントアウトを解除)
				#stream.stop_stream()
			except KeyboardInterrupt:
				break
		
		stream.stop_stream()
		stream.close()
		P.terminate()
		print('stopstream')
		