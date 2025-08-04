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



def loging(message):
    option, login, password = message.split(":")
    print(message.split(":"))
    if option == "1" and get_password_for_user(login, password):
        conn.sendall("AUTH:TRUE".encode())
    else:
        conn.sendall("AUTH:FALSE".encode())

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
