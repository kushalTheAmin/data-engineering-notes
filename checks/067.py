# checks for notes/067-json-types.md
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT customer_id, status FROM orders WHERE order_id = 103").fetchall() == [(1, 'delivered')]
assert con.execute("SELECT name, city FROM customers WHERE customer_id IN (1, 5) ORDER BY 1").fetchall() == [('Asha', 'Jersey City'), ('Esha', None)]
assert con.execute("SELECT stars FROM order_ratings WHERE order_id = 103").fetchall() == [(None,)]
# 7.50 khandvi + 3.00 masala chai, 1 each, in order 103
assert con.execute("SELECT sum(p.price * i.quantity) FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 103").fetchone()[0] == 10.5
assert con.execute("SELECT string_agg(p.name, ',' ORDER BY p.product_id) FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 103").fetchone()[0] == "khandvi,masala chai"
text = '{"order_id": 103, "customer": {"name": "Asha", "city": "Jersey City"}, "items": ["khandvi", "masala chai"], "total": 10.5, "delivered": true, "stars": null}'
d = json.loads(text)
assert [type(v).__name__ for v in d.values()] == ["int", "dict", "list", "float", "bool", "NoneType"]
assert len(d) == 6
try:
    json.loads('{"delivered": True}')
    raise SystemExit("True should fail")
except json.JSONDecodeError:
    pass
assert json.loads('{"c": null}')["c"] is None
assert json.loads('{"c": "null"}')["c"] == "null" and len("null") == 4
assert type(json.loads("10")) is int and type(json.loads("10.0")) is float
assert json.loads("0.1") + json.loads("0.2") != json.loads("0.3")
# source: https://www.rfc-editor.org/rfc/rfc8259
#   confirmed: a JSON value must be an object, array, number, or string, or one of false, null, true (lowercase); the literal names must be lowercase; no date type
# source: https://docs.python.org/3/library/json.html
#   confirmed: the json-to-python table maps number (int) to int and number (real) to float; the exponent form 1e2 coming back a float is asserted below
assert json.loads("1e2") == 100.0 and type(json.loads("1e2")) is float
assert int(10.50 * 100) == 1050
print("067 ok")
