import socket
import threading
import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

clients = {}

class VideoCamera:
    def __init__(self, client_id):
        self.video = cv2.VideoCapture(0)
        self.client_id = client_id
        (self.grabbed, self.frame) = self.video.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.video.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.video.release()

def handle_client(client_id):
    global clients
    if client_id not in clients:
        clients[client_id] = VideoCamera(client_id).start()
    camera = clients[client_id]
    while True:
        frame = camera.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/<client_id>')
def video_feed(client_id):
    return Response(handle_client(client_id), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def hello_world():
    return render_template("index.html")

if __name__=='__main__':
    app.run(threaded=True)
