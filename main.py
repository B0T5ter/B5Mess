import socket

SERVER_IP = '84.205.172.32'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, PORT))
    print("✅ Połączono z serwerem")

    message = "Szef testuje z zewnątrz 💀"
    client_socket.send(message.encode('utf-8'))

    print("📤 Wiadomość wysłana")
except Exception as e:
    print("❌ Błąd klienta:", e)
finally:
    client_socket.close()
