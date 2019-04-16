import socketio
sio =socketio.Client()

@sio.on('connect')
def on_connect():
    print('I\'m connected!')

@sio.on('message')
def on_message(data):
    print('I received a message!')

@sio.on('my message')
def on_message(data):
    print('I received a custom message!')

@sio.on('disconnect')
def on_disconnect():
    print('I\'m disconnected!')
try:
    sio.connect('https://push.aws.kambicdn.com/socket.io/?EIO=3&transport=websocket')
except Exception as e:
    print(e)