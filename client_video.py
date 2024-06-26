import pickle
import socket
import struct
import cv2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.111'  # Coloque o IP do servidor aqui
port = 9997
client_socket.connect((host_ip, port))

cap = cv2.VideoCapture('videoplayback.mkv')  # Usar um arquivo de vídeo

while cap.isOpened():
    print('enviando')
    ret, frame = cap.read()
    if not ret:
        print('break 1')
        break

    img_serialize = pickle.dumps(frame)
    message = struct.pack("Q", len(img_serialize)) + img_serialize
    client_socket.sendall(message)
    key = cv2.waitKey(10)
    if key == 27:
        print('break 2')
        break

cap.release()
client_socket.close()
cv2.destroyAllWindows()
