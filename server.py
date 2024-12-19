import grpc
from concurrent import futures
import time
import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []

    def SendMessage(self, request, context):
        sender = None
        for chat in request:
            if request.sender == None:
                self.clients.append(context)
                self.BroadCastMessage(chat.sender, "님이 접속했습니다.")
            else:
                self.BroadCastMessage(f"{chat.sender} : {chat.message}")

    def BroadCastMessage(self, sender, message):
        chat = chat_pb2.ChatMessage(
            sender = sender,
            message = message
        )
        for client in self.clients:
            client.SendMessage(chat)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    print("서버 실행 중")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
