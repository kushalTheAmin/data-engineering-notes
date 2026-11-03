# checks for notes/308-request-and-response-one-message-out-one-message-back.md
import os, sys, socket
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the body of the response is Ashas delivered orders, 101 and 103
rows = con.execute("SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'delivered' ORDER BY order_id").fetchall()
body = "[" + ", ".join(str(r[0]) for r in rows) + "]"
assert body == "[101, 103]"
assert len(body.encode()) == 10  # Content-Length: 10
assert body[:5] == "[101,"  # a client trusting Content-Length: 5 keeps only this
# check yourself 2: Ashas pending orders
rows = con.execute("SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'pending' ORDER BY order_id").fetchall()
assert rows == [(106,)]
assert len("[106]") == 5
# the request and response messages are CRLF separated with an empty line ending the head
req = b"GET /orders?customer_id=1&status=delivered HTTP/1.1\r\nHost: shop.example\r\n\r\n"
assert req.endswith(b"\r\n\r\n")
# source: https://www.rfc-editor.org/rfc/rfc9112.html
# confirmed: a message is start-line, header lines, an empty line, then an optional body; Content-Length gives the body length in octets; request-line is method SP request-target SP HTTP-version
# source: https://www.rfc-editor.org/rfc/rfc9110.html
# confirmed: HTTP is a stateless request/response protocol, a client sends a request message and the server responds
print("308 ok")
# audit: the note said plain HTTP is a few lines of text, which is true of HTTP/1.1 only. it now says HTTP/1.1 and that newer versions pack it as binary
# source: https://www.rfc-editor.org/rfc/rfc9113.txt
#   confirmed (opened this run): HTTP/2 enables more efficient processing of messages through use of binary message framing
