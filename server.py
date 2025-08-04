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

def get_friends(username, password):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname="B5Mlogin",
            user="postgres",
            password="twoje_haslo",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT znajomi FROM users WHERE username = %s AND password = %s;",
            (username, password)
        )
        result = cur.fetchone()
        if result:
            return result[0]  # to będzie tekst z kolumny znajomi
        else:
            return None
    except Exception as e:
        print("Błąd:", e)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def user_exists(username):
    try:
        conn = psycopg2.connect( ... )
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = %s LIMIT 1;", (username,))
        result = cur.fetchone()
        return result is not None  # True jeśli istnieje, False jeśli nie
    except Exception as e:
        print("Błąd:", e)
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

def add_friend(username, friend_login):
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

        # Pobieramy obecny string znajomych
        cur.execute("SELECT znajomi FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()

        if result is None:
            print("❌ Użytkownik nie istnieje")
            return False

        current_friends = result[0] or ""  # jeśli NULL, to pusty string

        # Sprawdź, czy znajomy już jest na liście (żeby nie dodawać duplikatów)
        friends_list = [f.strip() for f in current_friends.split(",") if f.strip()]
        if friend_login in friends_list:
            print(f"👀 {friend_login} już jest znajomym użytkownika {username}")
            return False

        # Dodajemy nowego znajomego
        friends_list.append(friend_login)
        new_friends_str = ",".join(friends_list)

        # Aktualizujemy w bazie
        cur.execute("UPDATE users SET znajomi = %s WHERE username = %s;", (new_friends_str, username))
        conn.commit()

        print(f"✅ Dodano {friend_login} do znajomych użytkownika {username}")
        return True

    except Exception as e:
        print("Błąd:", e)
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def handle_client(conn, addr):
    with conn:
        print(f"📥 Połączono z {addr}")
        message = conn.recv(1024).decode().strip()
        print("Odebrano:", message)

        try:
            option, username, password = message.split(":")
        except ValueError:
            conn.sendall("AUTH:FALSE".encode())
            return None

        if option == "1":
            if get_password_for_user(username, password):
                conn.sendall("AUTH:TRUE".encode())
                return username
            else:
                conn.sendall("AUTH:FALSE".encode())
                return None

        if option == "2":
            if add_new_user(username, password):
                conn.sendall("AUTH:TRUE".encode())
                return username
            else:
                conn.sendall("AUTH:FALSE".encode())
                return None

        if option == "3":
            friends = get_friends(username, password)
            if friends is None:
                friends = "No friends found"
            conn.sendall(friends.encode())
        
        if option == "4":
            # Sprawdzamy, czy właściciel konta istnieje
            if user_exists(password):  # password tu to login właściciela konta
                success = add_friend(password, username)  # dodajemy "username" jako znajomego do "password"
                if success:
                    conn.sendall("AUTH:TRUE".encode())
                else:
                    conn.sendall("AUTH:FALSE".encode())
            else:
                conn.sendall("AUTH:FALSE".encode())

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("🔐 Serwer logowania gotowy")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
