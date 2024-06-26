import os
import pickle
import socket
import struct
import threading
import cv2
from pyfiglet import Figlet

def handle_client(client_socket):
    vid = cv2.VideoCapture(0)
    while vid.isOpened():
        ret, image = vid.read()
        if not ret:
            break
        img_serialize = pickle.dumps(image)
        message = struct.pack("Q", len(img_serialize)) + img_serialize
        try:
            client_socket.sendall(message)
        except BrokenPipeError:
            break
        cv2.imshow('Video from Server', image)
        key = cv2.waitKey(10)
        if key == 27:
            break
    client_socket.close()
    vid.release()
    cv2.destroyAllWindows()

os.system("clear")
pyf = Figlet(font='puffy')
a = pyf.renderText("Video Chat App with Multi-Threading")
b = pyf.renderText("Server")
os.system("tput setaf 3")
print(a)

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP: \n HOST NAME:', host_ip, host_name)
port = 9999
socket_address = (host_ip, port)
# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
server_socket.listen(5)
print("Listening at:", socket_address)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('Connected to:', addr)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
