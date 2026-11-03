# checks for notes/307-urls-and-query-parameters.md
from urllib.parse import urlsplit, parse_qs
import sys
url = "http://shop.example:8080/orders?customer_id=1&status=delivered"
p = urlsplit(url)
assert (p.scheme, p.hostname, p.port, p.path) == ("http", "shop.example", 8080, "/orders")
assert parse_qs(p.query) == {"customer_id": ["1"], "status": ["delivered"]}
assert parse_qs("status=pending&status=delivered") == {"status": ["pending", "delivered"]}
# Ashas delivered orders from data/shop.sql are 101 and 103
import os
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
rows = shop().execute("SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'delivered' ORDER BY order_id").fetchall()
assert rows == [(101,), (103,)]
# source: https://docs.python.org/3/library/urllib.parse.html
# confirmed: parse_qs returns a dictionary whose values are lists of values for each name
# source: https://www.rfc-editor.org/rfc/rfc3986
# confirmed: the example foo://example.com:8042/over/there?name=ferret has scheme, host, port, path and a query, and query components are often key=value pairs
print("307 ok")
# audit: the note said the query is a list of key=value pairs, which reads as always true, but RFC 3986 says only that query components are often used to carry key=value pairs. it now says usually holds key=value pairs, often a dictionary written as text
# source: https://www.rfc-editor.org/rfc/rfc3986.txt
#   confirmed (opened this run): query components are often used to carry identifying information in the form of "key=value" pairs; a URI is a sequence of characters
# source: https://docs.python.org/3/library/urllib.parse.html
#   confirmed (opened this run): parse_qs separator defaults to '&'
