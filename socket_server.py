import socket
import json
import threading

#연결할 서버 주소와 포트 번호
host = '127.0.0.1'
port = 12345

#소켓 객체 생성, IPV4와 TCP 사용한다는 뜻
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#소켓 서버 연결
server_socket.bind((host, port))

#클라이언트와 연결
server_socket.listen(3)

#유저
users = []

print(f"{host} : {port}")

def chat(client_socket):
    name = client_socket.recv(1024)
    data = name.decode('utf-8') + '님 입장'
    print(data)

    try:
        for p in users:
            p.send(data.encode('utf-8'))

        while True:
            text = client_socket.recv(1024)
            data = name.decode('utf-8') + ":" + text.decode('utf-8')
            print(data)
            for p in users:
                p.send(data.encode('utf-8'))

    except:
        users.remove(client_socket)
        data = name.decode('utf-8') + "님 퇴장"
        print(data)
        if users:
            for p in users:
                p.send(data.encode('utf-8'))
        else:
            print('exit')


#무한루프
while True:
    #클라이언트 연결 대기
    client_socket, addr = server_socket.accept()
    users.append(client_socket)
    th = threading.Thread(target=chat, args=(client_socket,))
    th.start()

#소켓 종료
client_socket.close()
server_socket.close()