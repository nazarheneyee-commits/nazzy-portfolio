import os
import socket
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Silent or concise logging
        pass

class IPv6Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6

def start_server(server):
    try:
        server.serve_forever()
    except Exception:
        pass

if __name__ == "__main__":
    servers = []
    # Bind IPv4
    try:
        v4_server = ThreadingHTTPServer(('127.0.0.1', PORT), CustomHandler)
        servers.append(v4_server)
        threading.Thread(target=start_server, args=(v4_server,), daemon=True).start()
    except Exception as e:
        print(f"IPv4 bind failed: {e}")

    # Bind IPv6
    try:
        v6_server = IPv6Server(('::1', PORT), CustomHandler)
        servers.append(v6_server)
        threading.Thread(target=start_server, args=(v6_server,), daemon=True).start()
    except Exception as e:
        print(f"IPv6 bind failed: {e}")

    print(f"Server successfully running on port {PORT} (IPv4 + IPv6). Serving {DIRECTORY}", flush=True)

    # Keep main thread alive
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        for s in servers:
            s.server_close()
