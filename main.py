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


check = chceckInternet()
JSON = SaveJson()
audio = AudioPython()

hostMongo = '3.143.15.255:27017'

req = Request()
rasp = Control()
Ws = WebSocket()
mainSensor = Sensores()


global lastv, mongo

haveToken = False
token = ''

bandera = False


class Main:
    
    def hello():
        global haveToken, token, bandera
        
        conexion = check.check()
        

        if conexion:
            
            if haveToken == False:
                token = req.request()
                haveToken = True

            try:
                mongo = Peticiones_Mongo(hostMongo)
                sensores = mongo.getSensores()
            except:
                print('sin conexion con mongo')
            
            bandera = rasp.CheckRegado(token)
            print('bandera:',bandera)
        else:
            try:
                sensores = JSON.getDatos()
            except:
                print('No hay sensores gurdados')
        
        for sensor in sensores:
            mainSensor.setDatos(sensor,bandera)
            mainSensor.ejecutar()
        d = mainSensor.getDataSensores()
        
        print(f'------------------------------------dataaa: {d}')
        
        Ws.connect(d,'NivelP',token)
        respuesta = mainSensor.getRespuestas()
        print(respuesta)
        mongo.saveSensores(respuesta)
        mainSensor.cleerRespuesta()

if __name__ == '__main__':
    while True:
        Main.hello()
        os.system('clear')
        #GPIO.cleanup()
        time.sleep(1)
