import grpc
import chat_pb2
import chat_pb2_grpc
import os

def run():
    channel = grpc.insecure_channel('172.168.10.83:50051') #172.168.10.74, 83(my)
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    try:
        response = stub.SendMessage(generate_msg(user_name = input("이름을 입력하세요 :")))
        print('"help"를 입력하시면 사용자 커맨드를 확인할 수 있습니다')

        for res in response:
            print(f"{res.sender} : {res.message}")
    except Exception as e:
        print(e.details())


def generate_msg(user_name):
    join_msg = chat_pb2.ChatMessage(
        sender=user_name,
        message="채팅에 참여했습니다."
    )
    yield join_msg

    while True:
        message = input()
        if message == 'exit':
            break

        elif message == 'clear':
            os.system('cls')
            continue

        elif message == 'help':
            print("\n사용자 커맨드\n-clear:화면 지우기\n-exit:채팅 종료\n-users:온라인 사용자 목록 보기\n-귓 <유저이름> <메시지>:특정 사용자에게 개인 메시지 보내기\n")
            continue

        chat_msg = chat_pb2.ChatMessage(
            sender=user_name,
            message=message
        )

        yield chat_msg

if __name__ == '__main__':
    run()