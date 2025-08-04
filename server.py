import socket

# 🔐 Prosta baza danych użytkowników
users = {
    "filip": "haslo123",
    "admin": "root",
    "szefu": "1234"
}

HOST = '0.0.0.0'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("🔐 Serwer logowania gotowy")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"📥 Połączono z {addr}")
            try:
                data = conn.recv(1024).decode()
                if not data:
                    print("⚠️ Brak danych")
                    continue

                print(f"📨 Odebrano: {data}")
                try:
                    login, password = data.split(":")
                except ValueError:
                    conn.sendall("❌ Nieprawidłowy format danych".encode())
                    continue

                # ✅ Sprawdzanie danych logowania
                if login in users and users[login] == password:
                    response = "✅ Zalogowano pomyślnie"
                    print(f"✔️ Użytkownik {login} się zalogował")
                else:
                    response = "❌ Błędny login lub hasło"
                    print(f"❌ Nieudane logowanie z {addr}")

                conn.sendall(response.encode())

            except Exception as e:
                print("💥 Błąd:", e)
