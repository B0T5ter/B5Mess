import socket

HOST = '7.tcp.eu.ngrok.io'
PORT = 18374

#Logowanie
def loging():
    print("\nWelcome in B5Mess")
    print("1. Login")
    print("2. Sign up")
    while True:
        print("(input 1 or 2)")
        option = input(">")
        if option in ("1", "2"):
            break
        else:
            print("wrong option")
    
    #Login
    if option == "1":
        while True:
            login = input("login: ")
            password = input("password: ")
            message = f"{option}:{login}:{password}"
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            if "AUTH:TRUE" in response:
                print("Logged in")
                return
            else:
                print("Invalid login or password")
    
    #Sign up
    if option == "2":
        while True:
            login = input("login: ")
            password = input("password: ")
            message = f"{option}:{login}:{password}"
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            if "AUTH:TRUE" in response:
                print("Account created")
                return
            else:
                print("Account is already existing")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("🔗 Połączono z serwerem")
        loging()
        while True:
            # 📥 odbieranie wiadomości od serwera
            response = client_socket.recv(1024).decode()
            if not response:
                print("🛑 Serwer zakończył połączenie")
                break
            print(response)

            # 📤 wysyłanie wiadomości
            message = input(">")
            if message.lower() == "exit":
                print("👋 Kończę połączenie")
                break
            client_socket.sendall(message.encode())

except Exception as e:
    print("❌ Wystąpił błąd:", e)
