import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 12345))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

print("Server started on port", PORT)


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with", str(address))

        client.send("NAME".encode())
        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        print(name, "joined")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

