import os
from datetime import datetime
import time
import RPi.GPIO as GPIO
import requests
import json

#Variaveis globais:
NumeroAcionamentosBotao = 0

#GPIOs utilizados:
GPIOBotaoEmergencia = 18 #Broadcom pin 18 (P1 pin 12)

#Funcao: prepara I/Os
#Parametros: nenhum
#Retorno: nenhum
def PreparaIOs():
	#configura GPIO do botao como entrada e com pull up (do SoC Broadcom)
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(GPIOBotaoEmergencia, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return

#Funcao: envia notificacao via pushbullet
#Parametros: numero do acionamento do botao
#Retorno: nenhum
def EnviaNotificacaoPushbullet(Numero):
	now = datetime.now()
	StringDataHora = str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" em "+str(now.day)+"/"+str(now.month)+"/"+str(now.year)

	StringMsg = "Acionamento numero "+str(Numero)+" do botao de emergencia. Botao acionado por ultimo em "+StringDataHora+"."
	data_send = {"type": "note", "title": "Notificacao - botao emergencia", "body": StringMsg}
 
        ACCESS_TOKEN = 'tttttttttttttttttttttttttttttttttt'   #substituia "tttttttttttttttttttttttttttttttttt" pelo seu Acces Token
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})

	return

#Funcao: verifica acionamento e desacionamento do botao de emergencia
#Parametros: nenhum
#Retorno: nenhum
def VerificaBotaoEmergencia():
	global NumeroAcionamentosBotao

	#se o botao foi pressionado, envia a notificacao. 
	#caso contrario, nada e feito.
	if (GPIO.input(GPIOBotaoEmergencia) == 0):
		#Atualiza contagem de acionamentos e envia notificacao pelo pushbullet		
		NumeroAcionamentosBotao = NumeroAcionamentosBotao + 1
		EnviaNotificacaoPushbullet(NumeroAcionamentosBotao)		

		#delay para debouncing (50ms)
		time.sleep(0.050)

		#aguarda botao ser solto
		while (GPIO.input(GPIOBotaoEmergencia) == 0):
			continue

	return

#------------------------
#   Programa principal
#-----------------------
time.sleep(30)
PreparaIOs()

while True:
	VerificaBotaoEmergencia()