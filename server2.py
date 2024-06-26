import os
import pickle
import socket
import struct
import threading
import cv2
import queue
from pyfiglet import Figlet

# Fila para armazenar frames recebidos dos clientes
frames_queue = queue.Queue()

def handle_client(client_socket, i):
    data = b""
    metadata_size = struct.calcsize("Q")
    while True:
        while len(data) < metadata_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                return
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
        frames_queue.put((i, frame))

def display_frames():
    windows = {}
    while True:
        while not frames_queue.empty():
            i, frame = frames_queue.get()
            window_name = f'Video {i} from Server'
            if window_name not in windows:
                windows[window_name] = True  # Apenas para registrar a janela criada
            cv2.imshow(window_name, frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
port = 9993
socket_address = (host_ip, port)
# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
server_socket.listen(5)
print("Listening at:", socket_address)

index = 0
# Socket Accept
def accept_clients():
    global index
    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to:', addr)

        index += 1
        print('Launching another thread')
        client_handler = threading.Thread(target=handle_client, args=(client_socket, index))
        client_handler.start()

# Start a thread for accepting clients
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

# Run display_frames in the main thread
display_frames()
