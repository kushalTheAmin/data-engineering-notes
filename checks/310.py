# checks for notes/310-http-headers-notes-attached-to-a-request.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# Asha is customer 1, her delivered orders are 101 and 103, the body is [101, 103]
assert con.execute("SELECT name FROM customers WHERE customer_id = 1").fetchone()[0] == "Asha"
ids = [r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'delivered' ORDER BY order_id").fetchall()]
assert ids == [101, 103]
body = str(ids)
assert body == "[101, 103]" and len(body.encode()) == 10
# with status=delivered the body is exactly Ashas two delivered orders; without it order 106 (pending) would join in
all_ids=[r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall()]
assert all_ids == [101, 103, 106]
# the header loop
raw = "GET /orders HTTP/1.1\r\nHost: shop.example\r\nAccept: application/json\r\n\r\n"
headers = {}
for line in raw.split("\r\n\r\n")[0].split("\r\n")[1:]:
    name, value = line.split(": ", 1)
    headers[name.lower()] = value
assert headers == {"host": "shop.example", "accept": "application/json"}
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
# confirmed (section 5.1): field names are case-insensitive; (7.2) Host lets the origin server distinguish among resources while servicing requests for multiple host names; (12.5.1) Accept states preferences for response media types; (8.3) Content-Type indicates the media type of the content
# source: https://www.rfc-editor.org/rfc/rfc9112.txt
# confirmed (section 3.2): a client MUST send a Host header field in all HTTP/1.1 request messages
print("310 ok")
# audit: the note said most request headers say what the client wants and most response headers describe the body, which no page supports. it now says some of each
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
#   confirmed (opened this run, 10.1 and 10.2): request context fields give information about the user, user agent and resource behind the request; response context fields give information about the server, the target resource or related resources, so not all describe the body
