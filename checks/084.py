# checks for notes/084-a-network.md
m = "SET 106 delivered"
b = m.encode("utf-8")
assert len(b) == 17
assert b.hex(" ") == "53 45 54 20 31 30 36 20 64 65 6c 69 76 65 72 65 64"
assert b[-9:].hex(" ") == "64 65 6c 69 76 65 72 65 64"
assert b.decode("utf-8") == m
# source: https://www.postgresql.org/docs/current/protocol-overview.html
# confirmed: the first byte of a message identifies its type, the next four bytes give the length; "the very first message sent by the client (the startup message) has no initial message-type byte"
# source: https://www.rfc-editor.org/rfc/rfc9293
# confirmed: TCP is "ingesting a stream of bytes from a sending application and packetizing that stream of bytes into TCP segments"
print("084 ok")
