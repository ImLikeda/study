import socket
import json
import threading
import sys


def commun(socket):
    while True:
        data = socket.recv(1024)
        if not data: continue
        print(data.decode('utf-8'))

#버퍼 비우기
#sys.stdout.flush()

# 주소 설정
host = "127.0.0.1"
port = 12345

# 소켓 객체 생성, tcp랑 ipv4 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 설정된 주소로 입장
client_socket.connect((host, port))

#닉네임 설정
name = input('아이디 입력 :')

client_socket.send(name.encode('utf-8'))

#문자 전송
#client_socket.sendall('도롱도롱'.encode())

#JSON 전송
#send_data = {"user": 'like'}
#print(send_data)
#client_socket.sendall(json.dumps(send_data).encode())

thread = threading.Thread(target=commun, args=(client_socket,))
thread.start()

while True:
    text = input()
    #sys.stdout.flush()
    if not text:continue
    client_socket.send(text.encode('utf-8'))

#문자 수신
#data = client_socket.recv(1024)
#print('받음 :', data.decode())

client_socket.close()