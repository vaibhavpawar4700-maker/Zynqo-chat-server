import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("🚀 Zynqo Server Started...")

clients = []
usernames = []


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            broadcast(f"{username} left chat".encode())
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected:", address)

        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print("Username:", username)

        broadcast(f"{username} joined chat!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive()
