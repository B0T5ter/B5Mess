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
    try:
        conn.sendall("Welcome in B5Message\n".encode())
        conn.sendall("1. Log in\n".encode())
        conn.sendall("2. Sign up\n".encode())

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                # klient się rozłączył
                return None
            if data in ("1", "2"):
                break
            else:
                conn.sendall("Wybierz 1 lub 2\n".encode())

        if data == "1":
            while True:
                conn.sendall("Login: ".encode())
                login = conn.recv(1024).decode().strip()
                if not login:
                    return None

                conn.sendall("Password: ".encode())
                password = conn.recv(1024).decode().strip()
                if not password:
                    return None

                if get_password_for_user(login, password):
                    conn.sendall("✅ Zalogowano pomyślnie\n".encode())
                    return login
                else:
                    conn.sendall("Błędny login lub hasło, spróbuj jeszcze raz\n".encode())
        elif data == "2":
            while True:
                conn.sendall("Login: ".encode())
                login = conn.recv(1024).decode().strip()
                if not login:
                    return None

                conn.sendall("Password: ".encode())
                password = conn.recv(1024).decode().strip()
                if not password:
                    return None

                if add_new_user(login, password):
                    conn.sendall("✅ Konto utworzone pomyślnie\n".encode())
                    return login
                else:
                    conn.sendall("❌ Użytkownik istnieje lub błąd, spróbuj inny login\n".encode())
        else:
            conn.sendall("Nieznana opcja, rozłączam\n".encode())
            return None
    except (BrokenPipeError, ConnectionResetError):
        print("Klient rozłączył się przedwcześnie")
        return None
    
def handle_client(conn, addr):
    with conn:
        print(f"📥 Połączono z {addr}")
        login = loging(conn)
        if login:
            print(f"✔️ Użytkownik {login} się zalogował/rejestrował")
            # dalsza obsługa
        else:
            print(f"❌ Nieudane logowanie lub rozłączenie z {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🔐 Serwer logowania gotowy")

    while True:
        conn, addr = s.accept()
        # Tworzymy nowy wątek dla klienta
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
