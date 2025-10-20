import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(f"\n{message}")
        except:
            print("Terputus dari server.")
            break

def send_messages():
    while True:
        msg = input()
        client.send(msg.encode())

recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()