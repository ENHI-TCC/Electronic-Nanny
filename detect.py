import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
import sys
import os
import math
import matplotlib.ticker as mticker
import time
import alsaaudio



	 
limiar = 0.01	#limiar de energia que decide quando o microfone vai gravar
periodo = 70	
fs = 16000	#frequência de amostragem
grava = 0
jarbas = False
flag_comando = False
cont_gravacao = 0	

mqtt = 'sudo mosquitto_pub -h 192.168.100.33:1883 -t esp8266/lampadaLab -m desliga'

while(True):
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default')

	total_size = fs*1.1	#tempo de gravacao

	while total_size > 0:		
		# efetua uma leitura da porta de audio
		length, data = inp.read()
		# se a leitura trouxer dados, isto eh, l > 0, salva estas amostras no arquivo tmp.bin ou tmp2.bim
		if(length > 0):			
			# converte data para float32
			v = np.frombuffer(data, dtype=np.float32)
			# calcula a energia do quadro e, se for maior que o limiar, ativa a flag para gravar
			energy = np.dot(v,v) / float(len(v))
			# print("valor da energia", energy)
			if(energy > limiar and grava == 0):
				grava = 1
				print("Atingi a energia")
				
			if(grava == 1):	#grava durante 1,1 segundos
				
				total_size = total_size - length		
	grava = 0