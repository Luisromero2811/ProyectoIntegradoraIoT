from connection_websocket import *
from RequestLogin import *
from CheckConnectionInternet import *
from Mongo_Save import *
from Json_Save import *
# from Sensores import *
from RaspberryControl import *
from PlaySound import *
import time

Ws = WebSocket()
req = Request()
pet = Control()
check = chceckInternet()
JSON = SaveJson()
audio = AudioPython()

token = req.request()
hostMongo = '3.143.15.255:27017'


def hello():
    sen = ''
    valor = 0
    mongo = ''
    if check.check():
        print('entre')
        # d = int(input('numero'))
        # s = input('sala')
        # Ws.connect(d, s, token)

        """print(pet.checkPetLlenadoP(token))
        audio.playsound_pila_llena(pet.checkPetLlenadoP(token))
        audio.playsound_pila_vacia()
        audio.playsound_suelo_humedo(5)
        audio.playsound_suelo_seco()"""

        try:
            mongo = Peticiones_Mongo(hostMongo)
        except:
            print('Ocurrio un error con la base de datos')

        """try:
            if len(JSON.getDatos()) > 0:
                mongo.saveDatos(JSON.getDatos())
                JSON.clean_Datos()
        except:
            print('datos vacios')"""

        try:
            if len(JSON.getSensores()) > 0:
                print(JSON.getSensores())
                mongo.saveSensores(JSON.getSensores())
                JSON.clean_Sensores()
        except:
            print('sensores vacios')

        sen = mongo.getSensores()

    else:
        sen = JSON.getDatos()

    print(sen)
    JSON.clean_Datos()
    for s in sen:
        print(s)
        #sensor = Sensores()
        #sensor.setDatos(s)
        #sensor.ejecutar()

        JSON.store_json(s)

if __name__ == '__main__':
    while True:
        hello()
        time.sleep(1)
