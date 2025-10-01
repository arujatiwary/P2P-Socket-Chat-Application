# group_server.py
import socket, threading

HOST = '0.0.0.0'
PORT = 5050

clients = []
clients_lock = threading.Lock()

def broadcast(msg, exclude=None):
    with clients_lock:
        for c in clients:
            if c is exclude:
                continue
            try:
                c.sendall(msg)
            except:
                pass

def handle_client(conn, addr):
    print(f"New client {addr}")
    with conn:
        with clients_lock:
            clients.append(conn)
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                broadcast(data, exclude=conn)
        finally:
            with clients_lock:
                if conn in clients:
                    clients.remove(conn)
            print(f"Client {addr} disconnected")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Group server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
