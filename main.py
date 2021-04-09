import asyncio
import websockets
from connection_websocket import *
import WebSocketClient
from RequestLogin import *
from CheckConnectionInternet import *
from Mongo_Save import *
from Json_Save import *
import time

Ws = WebSocket()
req = Request()
check = chceckInternet()
JSON = SaveJson()

#token = req.request()
hostMongo = '3.143.15.255:27017'

def hello():
    """d = int(input('numero'))
    s = input('sala')
    Ws.connect(d,s)"""
    if check.check():
        mongo = Peticiones_Mongo(hostMongo)
    else:
        mongo = Peticiones_Mongo('127.0.0.1:27017')

    sen = mongo.getSensores()
    print(sen)
    for s in sen:
        print(s)
        JSON.save_sensors(s)
        #puertos = s['puertos'].split(',')
        #for puerto in puertos:
        #    print(puerto)
    #print(token)


if __name__ == '__main__':
    while True:
        hello()
        time.sleep(5)
