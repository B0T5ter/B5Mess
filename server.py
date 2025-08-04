import socket
import threading
import psycopg2

HOST = '0.0.0.0'
PORT = 12345

#Otwieranie bazy danych B5Mlogin
def get_password_for_user(username, pasw):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname="B5Mlogin",
            user="postgres",
            password="haslo123",
            host="localhost"
        )
        cur = conn.cursor()
        # używamy placeholdera %s żeby zabezpieczyć przed SQL injection
        cur.execute("SELECT password FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()
        if result:
            return result[0]  == pasw
        else:
            assert "użytkownik nie istnieje"

    except Exception as e:
        print("Błąd:", e)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def handle_client(conn, addr):
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
            return

        if get_password_for_user(login, password):
            print(f"✔️ Użytkownik {login} się zalogował")
            conn.sendall("✅ Zalogowano pomyślnie".encode())
        else:
            print(f"❌ Nieudane logowanie z {addr}")
            conn.sendall("❌ Błędny login lub hasło".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🔐 Serwer logowania gotowy")

    while True:
        conn, addr = s.accept()
        # Tworzymy nowy wątek dla klienta
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
