import socket
import threading

# Przykładowa baza użytkowników
users = {
    "filip": "haslo123",
    "admin": "admin123"
}

def handle_client(conn, addr):
    try:
        conn.sendall(b"LOGIN:")
        login = conn.recv(1024).decode().strip()

        conn.sendall(b"HASLO:")
        haslo = conn.recv(1024).decode().strip()

        if login in users and users[login] == haslo:
            conn.sendall(b"OK\n")
            print(f"{login} zalogowany z {addr}")
            # Dalej można rozwinąć: czat, komendy itp.
        else:
            conn.sendall(b"NIE\n")
            print(f"Nieudane logowanie z {addr}")

    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        conn.close()

HOST = '0.0.0.0'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🔐 Serwer logowania gotowy")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
