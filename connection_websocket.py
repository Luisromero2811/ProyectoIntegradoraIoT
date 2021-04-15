import asyncio

import websocket
from threading import Thread
import time
import json
import sys

data = ''


class WebSocket:
    dato = 0
    sala = ''
    datoMax = 0

    def on_message(self, ws, message):
        print(f'respuesta: {message}')

    def on_error(self, ws, error):
        pass

    def on_close(self, ws):
        print('### closed ###')

    def on_open(self,ws):
        def run(*args):
            data = {'t': 1, 'd': {'topic': self.sala}}
            self.ws.send(json.dumps(data))
            print('Envie el join')
            #while True:
            for i in range(1):
                time.sleep(1)
                data = {'t': 7, 'd': {'topic': self.sala, 'event': 'dato', 'data': self.dato}}
                self.ws.send(json.dumps(data))
            self.ws.close()
            print('terminating...')
        Thread(target=run).start()

    def connect(self, datoMin, sala,token):
        self.datoOld = self.dato
        self.dato = datoMin
        self.sala = sala
        count = True
        websocket.enableTrace(True)
        if len(sys.argv) < 2:
            host = f'ws://ec2-3-143-15-255.us-east-2.compute.amazonaws.com:3333/adonis-ws?token={token}'
        else:
            host = sys.argv[1]
        self.ws = websocket.WebSocketApp(host,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.on_open = self.on_open
        #print('antes de run')
        wst = Thread(target=self.ws.run_forever())
        wst.start()
        time.sleep(3)
        self.ws.keep_running = False
        wst.join()
        #print('despues de run')
