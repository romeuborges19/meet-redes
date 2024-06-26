import socket
import cv2
import pickle
import struct
from pyfiglet import Figlet
import os

# Clear terminal screen
os.system("clear")

# Render header text
pyf = Figlet(font='puffy')
a = pyf.renderText("Video Chat App without Multi-Threading")
b = pyf.renderText("Client")
os.system("tput setaf 3")
print(a)

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Server IP address
host_ip = '192.168.0.111'
port = 9992
client_socket.connect((host_ip, port))

data = b""
metadata_size = struct.calcsize("Q")

while True:
    while len(data) < metadata_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet

    if len(data) < metadata_size:
        break

    packed_msg_size = data[:metadata_size]
    data = data[metadata_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    key = cv2.waitKey(10)
    if key == 13:
        break

client_socket.close()
cv2.destroyAllWindows()
