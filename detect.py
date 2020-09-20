import numpy as np
import sys
import os
import math
import time
import alsaaudio
import requests
from datetime import datetime, timedelta

mqtt = 'sudo mosquitto_pub -h 192.168.100.33 -t bracelet/cry -m liga -r'	 #Publish Referente a confirmação de um choro
limiar = 0.01	#limiar de energia que decide quando o microfone vai gravar
periodo = 70	
fs = 16000	#frequência de amostragem
grava = 0

while(True):
	#possiveis configuracoes da placa de audio.
	#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default')
	#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 1)
	#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 2)
	
	# Configuração que funcionou melhor no Raspberry pi 3 B+ utilizando um microfone de abrangencia do tipo Omni.
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, channels=2, rate=44100, format=alsaaudio.PCM_FORMAT_FLOAT_LE, periodsize=70, device='default', cardindex= 1)

	total_size = fs*1.1	#tempo de gravacao

	while total_size > 0:		
		# efetua uma leitura da porta de audio
		length, data = inp.read()
		# se a leitura trouxer dados, isto eh, l > 0
		if(length > 0):			
			# converte data para float32
			v = np.frombuffer(data, dtype=np.float32)
			# calcula a energia do quadro e verifica se é maior que o limiar durante o periodo de tempo
			energy = np.dot(v,v) / float(len(v))
			# print(energy);
			#print("valor da energia", energy)
			if(energy > limiar):
				print("COMEÇOU")
				timeRightNow = datetime.now()
				furuteTime = timeRightNow + timedelta(seconds=4)
				print("tempo Inicial = ", timeRightNow)
				print("tempo Final = ", furuteTime)
				variavelContadora=0
				while(datetime.now() <= furuteTime):
					# print("Estou dentro do While")					
					if(energy > limiar and grava == 0):	
						variavelContadora += 1
						# print("Hora dentro do While = ", datetime.now())						
						if(datetime.now() >= furuteTime):
							print("")
							print("")
							print("*******Atingi a Energia*******")
							print("")
							print("")
							#requests.post('http://192.168.100.33:8080/ServerRequest/NewCry')
							os.system(mqtt)						
							grava = 1
					else:
						print("")
						print("")
						print("deu zica e nao atingi o limite")						
						print("")
						print("")
						grava = 0
						break
					# if(grava == 1):
					# 	grava = 0
				print("variavelContadora= ",variavelContadora)
				print("TERMINOU")