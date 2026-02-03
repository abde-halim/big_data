import socket, time, threading
print("test")
def start_socket_server():
    print("test2")

    host = "127.0.0.1"
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(1)
    print("🟢 Server waiting for connection...")
    conn, addr = s.accept()
    print("🟢 Client connected from:", addr)
    messages = ["spark streaming dstream", "spark spark streaming", "big data spark"]
    while True:
        for msg in messages:
            conn.send((msg + "\n").encode())
            time.sleep(2)
# threading.Thread(target=start_socket_server, daemon=True).start()
threading.Thread(target=start_socket_server).start()
