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
            return False

    except Exception as e:
        print("Błąd:", e)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#New user
def add_new_user(username, password):
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
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            (username, password)
        )
        conn.commit()  # zatwierdzamy zmiany w bazie
        print(f"Użytkownik {username} dodany pomyślnie")
        return True
    except psycopg2.errors.UniqueViolation:
        print(f"❌ Użytkownik {username} już istnieje")
        return False
    except Exception as e:
        print("Błąd:", e)
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def loging(conn):
    conn.sendall("Welcome in B5Message".encode())
    conn.sendall("1. Log in".encode())
    conn.sendall("2. Sign up".encode())

    while True:
        data = conn.recv(1024).decode().strip()
        if data in ("1", "2"):
            break
        else:
            conn.sendall("Wybierz 1 lub 2\n".encode())

    #Logowanie
    if data == "1":
        while True:
            conn.sendall("Login: ".encode())
            login = conn.recv(1024).decode().strip()

            conn.sendall("Password: ".encode())
            password = conn.recv(1024).decode().strip()

            if get_password_for_user(login, password):
                conn.sendall("✅ Zalogowano pomyślnie\n".encode())
                return login
            else:
                conn.sendall("Błędny login lub hasło, spróbuj jeszcze raz\n".encode())
    
    if data == "2":
        conn.sendall("Login: ".encode())
        login = conn.recv(1024).decode().strip()
        conn.sendall("Password: ".encode())
        password = conn.recv(1024).decode().strip()

        add_new_user(login, password)
        return login
    
def handle_client(conn, addr):
    with conn:
        print(f"📥 Połączono z {addr}")
        loging(conn)

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
