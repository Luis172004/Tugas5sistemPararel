import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = {}

def handle_client(client_socket, address):
    print(f"[+] {address} terhubung.")
    clients[client_socket] = address

    join_msg = f"{address} telah bergabung.\n".encode()
    broadcast(join_msg, None)

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break

            full_message = f"[{address}] {message.decode()}\n".encode()
            broadcast(full_message, client_socket)
    except:
        pass
    finally:
        print(f"[-] {address} terputus.")
        del clients[client_socket]
        client_socket.close()

        leave_msg = f"{address} telah keluar.\n".encode()
        broadcast(leave_msg, None)

def broadcast(message, sender_socket):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                del clients[client]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[SERVER] Listening di {HOST}:{PORT} ...")

while True:
    client_socket, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()
