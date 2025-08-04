import socket

HOST = '2.tcp.eu.ngrok.io'
PORT = 18167              

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("🔗 Połączono z serwerem")

        message = input("Wpisz wiadomość do wysłania: ")
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024)
        print("📨 Odpowiedź serwera:", response.decode())

except Exception as e:
    print("❌ Wystąpił błąd:", e)

