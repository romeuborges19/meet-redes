from typing import DefaultDict
from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO, emit
import time
import base64

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

@app.route('/video_feed/<client_id>')
def video_feed(client_id):
    global clients
    def generate():
        while True:
            if clients[client_id].get('frames'):
                frame = clients[client_id]['frames'].pop(0)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                time.sleep(0.1)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('register')
def handle_register(data):
    client_id = data['client_id']
    clients[client_id] = {'sid': request.sid}
    emit('response', {'message': f'Registered client {client_id}'})

@socketio.on('video')
def handle_video(data):
    global clients
    client_id = data['client_id']
    frame_data = data['frame']
    frame = base64.b64decode(frame_data.split(',')[1])
    clients[client_id] = {'frames': []}
    clients[client_id]['frames'].append(frame)

@socketio.on('number')
def handle_number():
    global client
    emit('count', {'number': list(clients.keys())})


if __name__ == '__main__':
    socketio.run(app, debug=True, host="192.168.179.7")
