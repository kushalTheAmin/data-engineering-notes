# checks for notes/086-client-and-server.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
assert con.execute("SELECT status FROM orders WHERE order_id = 107").fetchone()[0] == "delivered"
import socket
server = socket.socket()
server.bind(("127.0.0.1", 0))
server.listen()
port = server.getsockname()[1]
client = socket.create_connection(("127.0.0.1", port))
client.sendall(b"GET 107")
conn, _ = server.accept()
assert conn.recv(100).decode() == "GET 107"
conn.sendall(b"delivered")
assert client.recv(100).decode() == "delivered"
# source: https://docs.python.org/3/library/socket.html
# confirmed: listen() enables a server to accept connections, accept() waits for an incoming one, create_connection() connects to an address
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: Postgres uses a client/server model, a server process manages the database files and clients connect to it
# source: https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-bind
# confirmed: "For TCP/IP, if the port is specified as zero, the service provider assigns a unique port to the application"
# source: https://www.rfc-editor.org/rfc/rfc5321
# confirmed: "An SMTP session is initiated when a client opens a connection to a server and the server responds with an opening message"
# source: https://man7.org/linux/man-pages/man2/connect.2.html
# confirmed: ECONNREFUSED, "A connect() on a stream socket found no one listening on the remote address"
print("086 ok")
