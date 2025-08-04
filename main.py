import socket

# 🔌 Dane do połączenia z serwerem
HOST = '4.tcp.eu.ngrok.io'  # Adres serwera (np. ngrok)
PORT = 13007                # Port serwera

# 🔒 Dane logowania
login = input("Login: ")
password = input("Hasło: ")
credentials = f"{login}:{password}"

try:
    # ⚙️ Tworzenie połączenia TCP
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
