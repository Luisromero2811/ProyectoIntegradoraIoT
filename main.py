from connection_websocket import *
from RequestLogin import *
from CheckConnectionInternet import *
from Mongo_Save import *
from Json_Save import *
from Sensores import *
from RaspberryControl import *
from PlaySound import *
from RaspberryControl import *
from RPi import GPIO
import time
import os
from AlertWhatApp import *

check = chceckInternet()
JSON = SaveJson()
audio = AudioPython()

hostMongo = '3.143.15.255:27017'

msg = MessageAlert()
req = Request()
rasp = Control()
Ws = WebSocket()
mainSensor = Sensores()


global lastv, mongo

haveToken = False
token = ''

bandera = False
petLlenado = False

valorLlenado = 0
cantSensores = 0
isJoin = False
class Main:
    def join():
        global isJoin
        if isJoin == False:
            print('Para poder recibir notificaciones')
            print('debe de mandar un mensaje por medio de WhatsApp')
            print('numero: +1 415 523 8886 ')
            print('mensaje: join morning-public')
            y = input('Escriba Y/y cuando haya mandado el mensaje ')
            if y == 'Y' or y == 'y':    
                isJoin = True
    
    def hello():
        global haveToken, token, bandera,petLlenado, valorLlenado, cantSensores
        #JSON.save_sensors(True)
        conexion = check.check()
        if conexion:       

            try:
                if haveToken == False:
                    token = req.request()
                    haveToken = True
                    
            except Exception as e:
                print('no se pudo conectar con el servidor')
                print('Error: ', e)

            try:
                mongo = Peticiones_Mongo(hostMongo)
                sensores = mongo.getSensores()
                if len(sensores) > cantSensores:
                    cantSensores = len(sensores)
                    JSON.store_json(sensores)
                
            except:
                if len(sensores) > 0:
                    sensores = JSON.getDatos()
                print('sin conexion con mongo')
            
            try:
                if len(JSON.getSensores()) > 0:
                    data = JSON.getSensores()
                    mongo.saveSensores(data)
                    JSON.clean_Sensores()
            except:
                print('ocurrio un error al subir los datos locales')

            #try:
            if haveToken and conexion:
                bandera = rasp.CheckRegado(token)
                peticion = rasp.checkPetLlenadoP(token)
                petLlenado = peticion['llenar']
                valorLlenado = peticion['data']
            #$except:
             #   print('ocurrio un error al hacer las peticiones')
        else:
            try:
                sensores = JSON.getDatos()
                #print(sensores)
                time.sleep(3)
            except:
                print('No hay sensores gurdados')
        
        try:
            for sensor in sensores:
                #print(sensor)
                mainSensor.setDatos(sensor,bandera,petLlenado)
                mainSensor.ejecutar()
                done = mainSensor.checkDone(valorLlenado,65)
        except Exception as e:
            print('ocurrio un error al ejecutar los sensores, error: ',e)
        
        respuesta = mainSensor.getRespuestas()
        if conexion:
            d = mainSensor.getDataSensores()
        
            #msg.sendMessage('prueba de mensaje en rpi')
            try:
                Ws.connect(d,'NivelP',token)
            except:
                print('ocurrio un error al conectarse al websocket')
            try:
                mongo.saveSensores(respuesta)
            except:
                print('ocurrio un error al guardar los datos en mongo')
        else:
            if len(respuesta) > 0:
                JSON.save_sensors(respuesta)

        try:
            if conexion:
                valor = mainSensor.getDataSensores()
                if done['doneLlenado']:
                    audio.playsound_pila_llena(valorLlenado)
                    msg.sendMessage('la pila se ha llenado al ' + str(valor['NivelP']) + '%')
                    mainSensor.resetDoneL()
                if done['doneRegado']:
                    audio.playsound_suelo_humedo(valor['Humedad'])
                    msg.sendMessage('el suelo se ha regado al ' + str(valor['Humedad']) + '%')
                    mainSensor.resetDoneR()
                if done['doneMove']:
                    audio.playsound_move_detectado()
                    msg.sendMessage('se ha detectado movimiento')
                    mainSensor.resetDoneM()
            
        except:
            print('ocurrio un error al enviar la alerta')

        mainSensor.cleerRespuesta()
        

if __name__ == '__main__':
    while True:
        Main.join()
        Main.hello()
        os.system('clear')
        #GPIO.cleanup()
        time.sleep(1)
