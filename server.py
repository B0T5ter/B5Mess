import socket

users = {
    "filip": "haslo123",
    "admin": "root",
}

HOST = '0.0.0.0'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🔐 Serwer logowania gotowy")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"📥 Połączono z {addr}")
            data = conn.recv(1024).decode()
            print(f"DEBUG: Odebrano dane: '{data}'")

            try:
                login, password = data.split(":")
                print(f"DEBUG: Login: {login}, Hasło: {password}")
            except Exception as e:
                print(f"ERROR podczas splitowania: {e}")
                conn.sendall("❌ Nieprawidłowy format danych".encode())
                continue

            if login in users and users[login] == password:
                print(f"✔️ Użytkownik {login} się zalogował")
                conn.sendall("✅ Zalogowano pomyślnie".encode())
            else:
                print(f"❌ Nieudane logowanie z {addr}")
                conn.sendall("❌ Błędny login lub hasło".encode())
