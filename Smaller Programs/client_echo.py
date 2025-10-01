# client_echo.py
import socket  # Import the socket library

# Define server details
HOST = '127.0.0.1'  # The server's IP address (127.0.0.1 = localhost, same machine)
PORT = 5050         # The port number to connect to (must match server)

# Create a TCP socket (IPv4, Stream-based = TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server at (HOST, PORT)
    s.connect((HOST, PORT))
    
    # Send a message to the server
    # The message must be bytes, so prefix with b'' (binary literal)
    s.sendall(b'Hello, server!\n')
    
    # Wait to receive a response from the server
    # Reads up to 1024 bytes
    data = s.recv(1024)
    
    # Print the received message, decoded from bytes to string
    # repr() shows quotes and escape characters explicitly (e.g. '\n')
    print('Received', repr(data.decode()))