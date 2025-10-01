# chat_server_threaded.py
import socket, threading

# Server will listen on all network interfaces (0.0.0.0) at port 5050
HOST = '0.0.0.0'
PORT = 5050


# Thread function: read messages
def reader(conn, stop_event):
    try:
        while not stop_event.is_set():
            # Wait for incoming data from the client
            data = conn.recv(4096)
            if not data:  # empty means client disconnected
                print("\n[System] connection closed by peer.")
                stop_event.set()
                break
            # Print the message and re-show the prompt (> )
            print("\r" + data.decode().rstrip() + "\n> ", end="", flush=True)
    except Exception as e:
        print("\n[System] recv error:", e)
        stop_event.set()


# Thread function: send messages
def writer(conn, stop_event):
    try:
        while not stop_event.is_set():
            # Take input from the server user
            msg = input("> ")
            # If user types /quit, stop the loop
            if msg.strip() == "/quit":
                stop_event.set()
                break
            # Otherwise send the message to client
            conn.sendall((msg + "\n").encode())
    except Exception as e:
        print("\n[System] send error:", e)
        stop_event.set()

# -----------------------------
# Main server logic
# -----------------------------
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket to host:port
    s.bind((HOST, PORT))
    # Start listening for one connection
    s.listen(1)
    print(f"Listening on {HOST}:{PORT} ...")
    
    # Block until a client connects
    conn, addr = s.accept()
    print("Connected by", addr)
    
    # Use the new connection socket
    with conn:
        # Shared flag to signal threads to stop
        stop = threading.Event()
        
        # Start reader thread (listening for client messages)
        t1 = threading.Thread(target=reader, args=(conn, stop), daemon=True)
        # Start writer thread (taking input from this server user)
        t2 = threading.Thread(target=writer, args=(conn, stop), daemon=True)
        
        # Launch both threads
        t1.start(); t2.start()
        
        # Wait until both threads exit
        t1.join(); t2.join()
    
    print("Connection closed.")
