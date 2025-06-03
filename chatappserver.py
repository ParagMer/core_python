import socket
import threading

# List to hold all connected clients
clients = []
client_addresses = []

# Broadcast function to send messages to all connected clients
def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle client messages
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    client_addresses.append(client_address)

    # Inform other clients that a new user has joined
    broadcast_message(f"{client_address} has joined the chat!".encode(), client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Message from {client_address}: {message.decode()}")
                broadcast_message(message, client_socket)
            else:
                break
        except:
            break
    
    # Remove client from list and close connection
    print(f"Connection from {client_address} closed.")
    clients.remove(client_socket)
    client_addresses.remove(client_address)
    client_socket.close()
    broadcast_message(f"{client_address} has left the chat.".encode(), client_socket)

# Server setup
def start_server():
    host = '0.0.0.0'  # Accept connections from any IP
    port = 55555       # Port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
