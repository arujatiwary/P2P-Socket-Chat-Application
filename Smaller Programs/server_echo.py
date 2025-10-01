# server_echo.py
import socket  # Import the socket library (provides networking functions)

# Define server details
HOST = '0.0.0.0'   # "0.0.0.0" means listen on ALL available network interfaces
PORT = 5050        # Port number to listen on (must match the client)

# Create a TCP socket (IPv4, Stream-based = TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the given host and port so OS knows where to listen
    s.bind((HOST, PORT))
    
    # Put the socket into listening mode
    # Argument (1) = backlog size = how many incoming connections can wait
    s.listen(1)
    print(f"Listening on {HOST}:{PORT} ...")
    
    # Wait for a client to connect
    # accept() blocks until a client connects, then returns a new socket (conn) and the client address
    conn, addr = s.accept()
    
    # Work with the connection
    with conn:
        print('Connected by', addr)  # addr = (client_ip, client_port)
        
        # Communication loop
        while True:
            # Receive up to 1024 bytes of data from client
            data = conn.recv(1024)
            
            # If no data is received, client has closed the connection
            if not data:
                print("Connection closed by client.")
                break
            
            # Decode bytes into string and print (assumes UTF-8 text)
            print("Received:", data.decode().strip())
            
            # Echo the same data back to the client
            conn.sendall(data)