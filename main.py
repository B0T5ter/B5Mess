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
                return login, password
            else:
                print("Account is already existing")

def home_page(login, password):
    
    print("Main Page")
    print("1. Contacts list")
    print("2. Add contact")

    while True:
        print("(input 1 or 2)")
        option = input(">")
        if option in ("1", "2"):
            break
        else:
            print("wrong option")
    
    if option == "1":
        message = f"{3}:{login}:{password}"
        client_socket.sendall(message.encode())
        contacts = client_socket.recv(1024).decode()
        print(contacts)
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("🔗 Połączono z serwerem")
        login, password = loging()
        home_page(login, password)

except Exception as e:
    print("❌ Wystąpił błąd:", e)
