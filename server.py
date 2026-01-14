import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("Server started... Waiting for clients")

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client
def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            if client in clients:
                index = clients.index(client)
                username = usernames[index]
                clients.remove(client)
                usernames.remove(username)
                broadcast(f"{username} has left the chat.".encode('utf-8'))
                client.close()
            break

# Receive new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        # Ask client for username
        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)
        broadcast(f"{username} has joined the chat.".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

receive()
