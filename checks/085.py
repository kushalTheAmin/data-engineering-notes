# checks for notes/085-addresses-and-ports.md
ip = "192.0.2.10"
addr = bytes(int(p) for p in ip.split("."))
assert addr.hex(" ") == "c0 00 02 0a" and len(addr) == 4
port = bytes(divmod(5432, 256))
assert port.hex(" ") == "15 38" and len(port) == 2
assert 2 ** 16 == 65536 and 2 ** 16 - 1 == 65535
# source: https://www.postgresql.org/docs/current/runtime-config-connection.html
# confirmed: the TCP port the server listens on is 5432 by default and can be changed
# source: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv
# confirmed: https is port 443
# source: https://www.rfc-editor.org/rfc/rfc5737
# confirmed: 192.0.2.0/24 is a reserved documentation block (TEST-NET-1)
# source: https://www.rfc-editor.org/rfc/rfc791
# confirmed: an IPv4 address is 32 bits, four octets
# source: https://www.rfc-editor.org/rfc/rfc9293
# confirmed: TCP source and destination port numbers are 16 bits
# source: https://en.wikipedia.org/wiki/Port_(computer_networking)
# confirmed: "for TCP, port number 0 is reserved and cannot be used"
# source: https://man7.org/linux/man-pages/man2/connect.2.html
# confirmed: ECONNREFUSED, "A connect() on a stream socket found no one listening on the remote address"
# source: https://www.rfc-editor.org/rfc/rfc9293
# confirmed: if the connection does not exist (CLOSED), "a reset is sent in response to any incoming segment except another reset"
print("085 ok")
