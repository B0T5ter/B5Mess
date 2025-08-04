import socket


HOST = '2.tcp.eu.ngrok.io'
PORT = 18167              

# 🔒 Dane logowania
login = input("Login: ")
password = input("Hasło: ")
credentials = f"{login}:{password}"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Połączenie z serwerem
        print("🔗 Połączono z serwerem")

        # 📤 Wysyłanie danych logowania
        client_socket.sendall(credentials.encode())

        # 📥 Odbieranie odpowiedzi
        response = client_socket.recv(1024)
        print("📨 Odpowiedź serwera:", response.decode())

except Exception as e:
    print("❌ Wystąpił błąd:", e)
