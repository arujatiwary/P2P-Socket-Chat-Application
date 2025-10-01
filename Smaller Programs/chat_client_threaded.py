# chat_client_threaded.py
import socket, threading, sys

# Client will connect to localhost (127.0.0.1) on port 5050
# Change HOST to the server’s IP if running on different machines
HOST = '127.0.0.1'
PORT = 5050


# Thread function: read messages
def reader(sock, stop_event):
    try:
        while not stop_event.is_set():
            # Wait for incoming data from server
            data = sock.recv(4096)
            if not data:  # empty bytes = server closed connection
                print("\n[System] connection closed by peer.")
                stop_event.set()
                break
            # Print the message and redraw the prompt
            print("\r" + data.decode().rstrip() + "\n> ", end="", flush=True)
    except Exception as e:
        print("\n[System] recv error:", e)
        stop_event.set()


# Thread function: send messages
def writer(sock, stop_event):
    try:
        while not stop_event.is_set():
            # Take input from client user
            msg = input("> ")
            # If user types /quit, signal stop
            if msg.strip() == "/quit":
                stop_event.set()
                break
            # Otherwise, send message to server
            sock.sendall((msg + "\n").encode())
    except Exception as e:
        print("\n[System] send error:", e)
        stop_event.set()


# Main client logic
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to server
    s.connect((HOST, PORT))
    
    # Shared event to stop threads gracefully
    stop = threading.Event()
    
    # Start reader thread (receives messages from server)
    t1 = threading.Thread(target=reader, args=(s, stop), daemon=True)
    # Start writer thread (sends messages from this client)
    t2 = threading.Thread(target=writer, args=(s, stop), daemon=True)
    
    # Launch threads
    t1.start(); t2.start()
    
    # Wait until both threads exit
    t1.join(); t2.join()
    
    # Once threads end, close connection and print status
    print("Disconnected.")