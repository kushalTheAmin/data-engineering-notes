# 085: addresses and ports, the right program on the right machine
builds on: [004 bytes](./004-bytes.md), [050 processes](./050-processes.md), [084 a network, computers sending bytes to each other](./084-a-network.md)
section: tables, keys and relationships, part 7, ~2 min read

Ashas 17 bytes are on the wire, but the server machine runs a database, a web server and plenty more at once. so which one gets them?

two numbers decide it. an address picks the machine, a port picks the [process](./050-processes.md) (one running program) on it. i think of the address as the building and the port as the flat number.

```text
Ashas phone  ->  192.0.2.10 : 5432
                 -----------   ----
                 which machine  which program

192.0.2.10 : 5432   the database
192.0.2.10 : 443    the web server
192.0.2.10 : 22     not running, so "connection refused"
```

both numbers travel as [bytes](./004-bytes.md), groups of 8 bits, in front of the message. the dotted kind of address (IPv4) is 4 bytes, a port is 2:

```python
ip = "192.0.2.10"
addr = bytes(int(part) for part in ip.split("."))
port = bytes(divmod(5432, 256))
print(addr.hex(" "), len(addr))
print(port.hex(" "), len(port))
```

```output
c0 00 02 0a 4
15 38 2
```

two bytes hold 65536 different values, so port numbers run from 0 to 65535 (tcp reserves 0, so a real connection uses 1 and up). 192.0.2.10 is a reserved example address, real ones look the same, and you usually type a name that gets looked up as one.

5432 is where Postgres listens unless someone changes it, and 443 is where https traffic goes. those are habits, not laws. i assumed the address alone found the database, but it only gets you to the building.

the bug this explains: "connection refused" usually means the machine answered and nothing listens on that port. a wrong port is not the same problem as a server that is down.

the next one is who starts the conversation, the asker or the answerer.

---
prev: [084 a network, computers sending bytes to each other](./084-a-network.md) | next: [086 client and server](./086-client-and-server.md)
