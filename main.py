import socket

HOST = '4.tcp.eu.ngrok.io'  # <-- tu wstaw swój z ngrok
PORT = 13007                # <-- tu też swój

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# --- LOGIN ---
login = input("Login: ")
haslo = input("Hasło: ")

wiadomosc = f"{login}:{haslo}"
client_socket.send(wiadomosc.encode())  # wysyłasz login i hasło

odpowiedz = client_socket.recv(1024).decode()
print("Serwer mówi:", odpowiedz)

client_socket.close()