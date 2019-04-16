import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

import json

def on_message(ws, message):
    print(message.decode("utf-8"))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(1)
            ws.send('2')
            #ws.send(json.dumps(info))
            ws.send('pong')
            ws.send('{"subscribe", {topic: "v2018.ub.ev.json"}}')
            ws.send('{"subscribe", {topic: "v2018.ub.en.ev.json"}}')

        time.sleep(1)
        #ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://push.aws.kambicdn.com/socket.io/?EIO=3&transport=websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()