import numpy as np
import sys
import os
import math
import time
import alsaaudio
import requests

mqtt = 'sudo mosquitto_pub -h 192.168.100.33 -t bracelet/cry -m liga -r'	 
limiar = 0.02	#limiar de energia que decide quando o microfone vai gravar
periodo = 70	
fs = 16000	#frequência de amostragem
grava = 0


while(True):
	#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default')
	# inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 1)

	# inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 2)
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, channels=2, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 1)

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
			# print(energy);
			#print("valor da energia", energy)
			if(energy > limiar and grava == 0):
				print("atingi a energia")
				requests.post('http://192.168.100.33:8080/ServerRequest/NewCry')
				os.system(mqtt)
				grava = 1
			if(grava == 1):
				grava = 0

