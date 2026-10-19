# 086: client and server, you ask, the database answers
builds on: [082 a database, a program that guards your data](./082-a-database-guards-the-data.md), [084 a network, computers sending bytes to each other](./084-a-network.md), [085 addresses and ports, the right program on the right machine](./085-addresses-and-ports.md)
section: tables, keys and relationships, part 8, ~2 min read

when Asha checks an order, who talks first, her phone or the database? i assumed it was between equals, and it never is.

a server is a program that waits for requests, and a client is a program that sends one. the server picks a [port](./085-addresses-and-ports.md) (a number naming one program on a machine) and listens on it. the client knocks, the server answers on that same connection. here is the whole thing with order 107 of the shop (the imaginary snack store), which is delivered, both ends in one script (the [network](./084-a-network.md) here is just this machine talking to itself):

```python
import socket

server = socket.socket()
server.bind(("127.0.0.1", 0))  # 127.0.0.1 is this same machine, 0 means any free port
server.listen()                # now it waits for someone to knock
port = server.getsockname()[1]

client = socket.create_connection(("127.0.0.1", port))  # the client starts it
client.sendall(b"GET 107")
conn, _ = server.accept()      # the server picks up the knock
print("server got:", conn.recv(100).decode())
conn.sendall(b"delivered")
print("client got:", client.recv(100).decode())
```

```output
server got: GET 107
client got: delivered
```

the server had to be listening before the client could knock, and it never starts the connection (some protocols have it greet you right after the knock, but the knock still comes first). that is the connection refused from [085](./085-addresses-and-ports.md): the knock landed where nobody listens. the [database](./082-a-database-guards-the-data.md) from 082 is a server, so Ashas phone and Bhavins phone are two clients asking one program.

client and server are roles, not machines. your laptop can run both at once, and a web server is a server to the browser but a client when it asks the database for rows. at my react and .NET day job the browser is the client and the API is the server, and the API is then a client of the database. i thought a server meant a big special computer, but it only means the side that waits.

---
prev: [085 addresses and ports, the right program on the right machine](./085-addresses-and-ports.md) | next: [087 primary key, one unique id per row](./087-primary-key.md)
