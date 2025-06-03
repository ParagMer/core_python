import socket
import threading

# Handle receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode())
            else:
                break
        except:
            break

# Send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        if message:
            client_socket.send(message.encode())

# Client setup
def start_client():
    host = input("Enter server IP address: ")  # Enter server's IP address
    port = 55555  # Port number to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to the server at {host}:{port}")

    # Start receiving messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Start sending messages to the server
    send_messages(client_socket)

if __name__ == "__main__":
    start_client()
