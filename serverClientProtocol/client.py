import socket
import time
import interface  # Import the interface module

# Define host and port
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

connected = False
inter = interface.Interface()
# Retry connecting to the server until successful
while not connected:
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            client_socket.connect((HOST, PORT))
            print("Connected to the server")
            connected = True

            # Receive data from the server
            data = client_socket.recv(1024)

            # Check if the server requests the login menu
            if data == b'SHOW_LOGIN_MENU':
                # Activate the login menu by calling the function from the interface module
                interface.login_menu(client_socket)

    except ConnectionRefusedError:
        print("Connection refused. Retrying in 1 second...")
        time.sleep(1)
