import socket
import threading

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def send_user_list():
    users = "USERS:" + ",".join(usernames)
    broadcast(users.encode())

def handle(client):
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

            send_user_list()
            break

def receive():
    print("Server started...")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print(f"Username is {username}")

        send_user_list()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
