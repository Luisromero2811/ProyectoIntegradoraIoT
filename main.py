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

class Main:
    
    def hello():
        global haveToken, token, bandera,petLlenado
        
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
                
            except:
                if len(sensores) > 0:
                    sensores = JSON.getDatos()
                print('sin conexion con mongo')
            
            try:
                if len(JSON.getSensores()) > 0:
                    data = JSON.getSensores()
                    mongo.saveSensores(data)
            except:
                print('ocurrio un error al subir los datos locales')

            try:
                if haveToken and conexion:
                    bandera = rasp.CheckRegado(token)
                    petLlenado = rasp.checkPetLlenadoP(token)
            except:
                print('ocurrio un error al hacer las peticiones')

        else:
            try:
                sensores = JSON.getDatos()
            except:
                print('No hay sensores gurdados')
        
        try:
            for sensor in sensores:
                mainSensor.setDatos(sensor,bandera,petLlenado)
                mainSensor.ejecutar()
        except:
            print('ocurrio un error al ejecutar los sensores')
        
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
            JSON.save_sensors(respuesta)
        mainSensor.cleerRespuesta()

if __name__ == '__main__':
    while True:
        Main.hello()
        os.system('clear')
        #GPIO.cleanup()
        time.sleep(1)
