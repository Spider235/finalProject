import socket
import pygame

# Define host and port
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print("Connected to the server")

