# client.py
import socket

HOST = '4.tcp.eu.ngrok.io'
PORT = 18298

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print("🔌 Połączono z serwerem!")

    while True:
        message = input("💬 Wpisz wiadomość (lub 'exit'): ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        print(f"📩 Odpowiedź: {data}")

except Exception as e:
    print(f"❌ Błąd klienta: {e}")

finally:
    client_socket.close()
