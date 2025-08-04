import socket

# IP serwera (czyli komputera, który odpalił serwer)
HOST = '192.168.50.188'  # <- zamień na IP serwera w Twojej sieci
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

wiadomosc = "Halo, tu klient 🚀"
client_socket.send(wiadomosc.encode())

client_socket.close()
