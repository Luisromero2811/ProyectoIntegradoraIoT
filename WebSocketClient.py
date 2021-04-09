import websocket
import asyncio
import json


class WebSocket:
    def connect(self):
        ws = websocket.create_connection('ws://ec2-3-143-15-255.us-east-2.compute.amazonaws.com:3333/adonis-ws')
        data = {'t':1,'d':{'topic':'NivelP'}}
        ws.send(json.dumps(data))

        res = ws.recv()
        res = json.loads(res)
        print(res)



    def join(self):
        ws = websocket.create_connection('ws://ec2-3-143-15-255.us-east-2.compute.amazonaws.com:3333/adonis-ws')
        ws.send(json.dumps({
            'event':'subscribe',
            'subscription':'NivelP'
        }))
        res = ws.recv()
        res = json.loads(res)
        print(res)

    def send(self):
        ws = websocket.create_connection('ws://ec2-3-143-15-255.us-east-2.compute.amazonaws.com:3333/adonis-ws')
        ws.send(json.dumps({
            'event':'subscribe',
            'subscription':'NivelP',
            'data':{
                'dato':5
            }
        }))
        res = ws.recv()
        res = json.loads(res)
        print(res)
