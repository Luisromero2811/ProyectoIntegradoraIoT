from connection_websocket import *
from RequestLogin import *
from CheckConnectionInternet import *
from Mongo_Save import *
from Json_Save import *
# from Sensores import *
from RaspberryControl import *
import time

Ws = WebSocket()
req = Request()
pet = Control()
check = chceckInternet()
JSON = SaveJson()

token = req.request()
hostMongo = '3.143.15.255:27017'


def hello():
    sen = ''

    if check.check():
        # d = int(input('numero'))
        # s = input('sala')
        # Ws.connect(30, 'NivelP', token)
        print(pet.checkPetLlenadoP(token))
        mongo = Peticiones_Mongo(hostMongo)
        if len(JSON.getSensores()) > 0:
            mongo.saveSensores(JSON.getSensores())
            JSON.clean_Sensores()
        else:
            return False

        sen = mongo.getSensores()

    else:
        sen = JSON.getDatos()

    print(sen)
    """for s in sen:
        print(s)
        sensor = Sensores()
        sensor.setDatos(s)
        #sensor.ejecutar()

        #JSON.store_json(s)"""


if __name__ == '__main__':
    while True:
        hello()
        time.sleep(1)
