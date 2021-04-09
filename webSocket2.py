import websocket
from threading import Thread
import time
import sys
import json

import codecs


encoding ="utf-8"
nbytes = {
    'utf-8': 1,
    'utf-16': 2,
    'utf-32': 4,
}.get(encoding, 1)


def to_hex(t, nbytes):
    """Format text t as a sequence of nbyte long values
    separated by spaces.
    """
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    return b' '.join(
        hex_version[start:start + chars_per_item]
        for start in range(0, len(hex_version), chars_per_item)
    )



data=""

def on_message(ws, message):
    print("*"*20)
    print(message)


def on_error(ws, error):
    #print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        data={"t":1,"d":{"topic":"NivelP"}}
        ws.send(json.dumps(data))
        while True:
        #for i in range(6):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            dat = int(input('numero'))
            data={"t":7,"d":{"topic":"NivelP","event":"dato","data":dat}}
            ws.send(json.dumps(data))
            #ws.send("Hello %d" % i)
            time.sleep(10)

        time.sleep(1)
        #ws.close()
        #print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = f"ws://ec2-3-143-15-255.us-east-2.compute.amazonaws.com:3333/adonis-ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2MDY1MTE5ZjY4OTY4ZjBhMDg4ZDU0NDciLCJpYXQiOjE2MTc2NjAyODZ9.bkExyxpxqcI3jCfcWP3Evz50SGwNUPW5hq98o7BnLus"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.on_open = on_open


    ws.run_forever()

