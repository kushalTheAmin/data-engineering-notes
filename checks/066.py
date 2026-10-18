# checks for notes/066-json-records-with-names-on-every-value.md
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
o = con.execute("SELECT order_id, customer_id, CAST(ordered_at AS VARCHAR), status FROM orders WHERE order_id = 101").fetchall()
assert o == [(101, 1, '2026-04-01 09:15:00', 'delivered')]
a = '{"order_id": 101, "customer_id": 1, "ordered_at": "2026-04-01 09:15:00", "status": "delivered"}'
b = '{"status": "delivered", "ordered_at": "2026-04-01 09:15:00", "customer_id": 1, "order_id": 101}'
assert json.loads(a)["status"] == json.loads(b)["status"] == "delivered"
assert json.loads(a) == json.loads(b)
assert len("101,1,2026-04-01 09:15:00,delivered") == 35 and len(a) == 95
try:
    json.loads("{'order_id': 101}")
    raise SystemExit("single quotes should fail")
except json.JSONDecodeError:
    pass
# source: https://www.rfc-editor.org/rfc/rfc8259
#   confirmed: an object is an unordered collection of zero or more name/value pairs; the abstract calls JSON a lightweight, text-based, language-independent data interchange format; a string begins and ends with quotation marks (double quote, %x22)
assert type(json.loads(a)["order_id"]) is int
print("066 ok")
