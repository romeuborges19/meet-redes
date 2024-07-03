import pickle
import socket
import struct
import cv2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.111'  # Coloque o IP do servidor aqui
port = 9993
client_socket.connect((host_ip, port))

cap = cv2.VideoCapture(0)  # Usar um arquivo de vídeo

while cap.isOpened():
    print('enviando')
    ret, image = cap.read()
    if not ret:
        break

    ret, buffer = cv2.imencode('.jpg', image)
    frame = buffer.tobytes()

    # img_serialize = pickle.dumps(image)
    # message = struct.pack("Q", len(img_serialize)) + img_serialize

    try:
        client_socket.sendall(frame)
    except BrokenPipeError:
        print(f'broken pipe')
        break

client_socket.close()
cv2.destroyAllWindows()
