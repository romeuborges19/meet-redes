import os
import pickle
import socket
import struct
import threading
import cv2
from pyfiglet import Figlet

def handle_client(client_socket, client_id):
    while True:
        data = b""
        payload_size = struct.calcsize("Q")
        
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet
        
        if len(data) < payload_size:
            break
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        
        frame_data = data[:msg_size]
        frame = pickle.loads(frame_data)
        
        cv2.imshow(f'Client {client_id}', frame)
        if cv2.waitKey(10) == 27:  # Pressione 'Esc' para fechar
            break

    client_socket.close()
    cv2.destroyWindow(f'Client {client_id}')

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
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
server_socket.listen(5)
print("Listening at:", socket_address)

client_id = 0

while True:
    client_socket, addr = server_socket.accept()
    print('Connected to:', addr)
    client_id += 1
    print('Client ID:', client_id)
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id))
    client_handler.start()
