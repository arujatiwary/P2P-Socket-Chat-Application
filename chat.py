# chat.py - Peer-to-peer chat with file transfer
import socket, threading, argparse, sys, os

BUFFER_SIZE = 4096  # number of bytes to read/write at a time

# Function: receive messages
def recv_loop(conn, stop_event):
    try:
        while not stop_event.is_set():
            # Try to read from the socket
            data = conn.recv(BUFFER_SIZE)
            if not data:  # empty bytes = peer disconnected
                print("\n[System] Peer disconnected.")
                stop_event.set()
                break

            # Decode into string (ignore invalid bytes)
            line = data.decode(errors="ignore").rstrip()

            # If it's a file transfer header
            if line.startswith("/file "):
                try:
                    # Extract filename and size from header
                    _, filename, size_str = line.split(" ", 2)
                    size = int(size_str)
                except Exception:
                    print("[System] Malformed file header.")
                    continue

                print(f"\n[System] Incoming file {filename} ({size} bytes)...")

                # Read exactly `size` bytes (the file contents)
                filedata = b""
                while len(filedata) < size:
                    chunk = conn.recv(min(BUFFER_SIZE, size - len(filedata)))
                    if not chunk:
                        break
                    filedata += chunk

                # Save file to "received_files" directory
                os.makedirs("received_files", exist_ok=True)
                filepath = os.path.join("received_files", filename)
                with open(filepath, "wb") as f:
                    f.write(filedata)

                print(f"[System] File saved to {filepath}\n> ", end="", flush=True)
                continue  # go back to waiting for new messages

            # Otherwise, it's just a normal chat message
            print("\r" + line + "\n> ", end="", flush=True)

    except Exception as e:
        if not stop_event.is_set():
            print("\n[System] recv error:", e)
            stop_event.set()


# Function: send messages
def send_loop(conn, stop_event, name):
    try:
        while not stop_event.is_set():
            try:
                msg = input("> ")  # read user input
            except EOFError:
                stop_event.set()
                break

            # Quit command
            if msg.strip() == "/quit":
                try:
                    conn.sendall(f"[{name}] has left the chat.\n".encode())
                except:
                    pass
                stop_event.set()
                break

            # File sending
            if msg.startswith("/send "):
                filepath = msg.split(" ", 1)[1]
                if not os.path.exists(filepath):
                    print("[System] File not found.")
                    continue
                size = os.path.getsize(filepath)
                filename = os.path.basename(filepath)

                try:
                    # Send header first
                    conn.sendall(f"/file {filename} {size}\n".encode())
                    # Send file in chunks
                    with open(filepath, "rb") as f:
                        while True:
                            chunk = f.read(BUFFER_SIZE)
                            if not chunk:
                                break
                            conn.sendall(chunk)
                    print(f"[System] Sent file {filename} ({size} bytes)")
                except Exception as e:
                    print("[System] File send failed:", e)
                    stop_event.set()
                continue  # skip to next input

            # Normal message
            try:
                conn.sendall(f"[{name}] {msg}\n".encode())
            except Exception as e:
                print("\n[System] send error:", e)
                stop_event.set()
                break

    except Exception as e:
        print("\n[System] send loop error:", e)
        stop_event.set()


# Run in "listen" mode
def run_listen(host, port, name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)  # wait for one connection
        print(f"[System] Listening on {host}:{port} ...")
        conn, addr = s.accept()
        print(f"[System] Connected by {addr}")
        with conn:
            stop = threading.Event()
            # Start one thread for receiving, one for sending
            r = threading.Thread(target=recv_loop, args=(conn, stop), daemon=True)
            w = threading.Thread(target=send_loop, args=(conn, stop, name), daemon=True)
            r.start(); w.start()
            r.join(); w.join()


# Run in "connect" mode
def run_connect(host, port, name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[System] Connected to {host}:{port}")
        stop = threading.Event()
        r = threading.Thread(target=recv_loop, args=(s, stop), daemon=True)
        w = threading.Thread(target=send_loop, args=(s, stop, name), daemon=True)
        r.start(); w.start()
        r.join(); w.join()


# Entry point
def main():
    parser = argparse.ArgumentParser(description="Peer-to-peer chat with file transfer")
    sub = parser.add_subparsers(dest="mode", required=True)

    # Sub-command: listen
    listen = sub.add_parser("listen")
    listen.add_argument("--host", default="0.0.0.0")
    listen.add_argument("--port", type=int, default=5050)
    listen.add_argument("--name", default="Anonymous")

    # Sub-command: connect
    connect = sub.add_parser("connect")
    connect.add_argument("host")
    connect.add_argument("port", type=int)
    connect.add_argument("--name", default="Anonymous")

    args = parser.parse_args()

    try:
        if args.mode == "listen":
            run_listen(args.host, args.port, args.name)
        else:
            run_connect(args.host, args.port, args.name)
    except KeyboardInterrupt:
        print("\n[System] Interrupted by user.")
    except Exception as e:
        print(f"[System] Error: {e}")
    finally:
        print("[System] Exiting.")

if __name__ == "__main__":
    main()