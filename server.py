# server.py
import socket

HOST = '0.0.0.0'  # nasłuchuj na wszystkich interfejsach
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"🟢 Serwer nasłuchuje na {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"📞 Połączono z: {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"📨 Otrzymano wiadomość: {data}")
    conn.sendall("✔️ Odebrano wiadomość!".encode())

conn.close()
server_socket.close()
