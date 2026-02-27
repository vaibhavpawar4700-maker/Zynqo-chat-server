import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
usernames = []


def broadcast_users():
    users = ",".join(usernames)
    for client in clients.values():
        client.send(f"USERS:{users}".encode())


def handle(client, username):
    while True:
        try:
            message = client.recv(1024).decode()

            if message.startswith("@"):
                target, msg = message.split(":", 1)
                target_user = target.replace("@", "")

                if target_user in clients:
                    clients[target_user].send(
                        f"{username}: {msg}".encode()
                    )
            else:
                for user, conn in clients.items():
                    conn.send(f"{username}: {message}".encode())

        except:
            del clients[username]
            usernames.remove(username)
            broadcast_users()
            client.close()
            break


def receive():
    print("Server started...")

    while True:
        client, address = server.accept()
        print("Connected:", address)

        client.send("NAME".encode())
        username = client.recv(1024).decode()

        clients[username] = client
        usernames.append(username)

        broadcast_users()

        thread = threading.Thread(
            target=handle,
            args=(client, username)
        )
        thread.start()


receive()