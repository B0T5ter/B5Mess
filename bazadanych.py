import psycopg2

try:
    # łączenie z bazą
    conn = psycopg2.connect(
        dbname="B5Mlogin",
        user="postgres",
        password="haslo123",  # wpisz swoje hasło
        host="localhost",
        port=5432
    )

    cur = conn.cursor()

    # wykonaj zapytanie, np. pobierz wszystkich userów
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()

    print("Zawartość tabeli users:")
    for row in rows:
        print(row)

except Exception as e:
    print("Błąd podczas pracy z bazą:", e)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
