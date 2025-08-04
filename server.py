import socket

# Tworzymy gniazdo
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# BIND: przypisujemy IP i port (host = '0.0.0.0' nasłuchuje na wszystkich interfejsach)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)

print("Serwer nasłuchuje... 🕵️")

# Akceptujemy połączenie
conn, addr = server_socket.accept()
print(f"Połączono z: {addr}")

while True:
    data = conn.recv(1024)  # odbieramy dane
    if not data:
        break
    print("📨 Otrzymano wiadomość:", data.decode())

conn.close()
server_socket.close()