import socket
import threading



def find_usable_port():
    listen_socket = socket.socket()
    amogus = 'h'
    for ip in range(0,255):
        for port in range(1024,65536):
            try:
                print(f"Trying 127.0.0.{ip}, port {port}")
                listen_socket.bind((f'127.0.0.{ip}',port))
                listen_socket.listen()
            except Exception as e:
                print(e)
            else:
                amogus = 'l bozo'
                break
        if amogus != 'h':
            break

    return ((f'127.0.0.{ip}',port))



# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = find_usable_port()  # Replace with the desired server IP address and port
server_socket.bind(server_address)
server_socket.listen(5)

clients = []

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Receive data from the client
            if data:
                print(f'Received message from {client_address}: {data}')
                # Broadcast the received message to all clients
                for client in clients:
                    if client != client_socket:
                        client.sendall(data.encode())
        except Exception as e:
            print(f'Error occurred while handling client {client_address}: {str(e)}')
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f'Connected with {client_address}')
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    print('Server started at ', server_address)
    start_server()
