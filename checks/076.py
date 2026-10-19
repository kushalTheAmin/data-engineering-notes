# checks for notes/076-data-types-in-a-schema.md
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 104").fetchall() == [("dhokla", 3)]
assert 3 * 2 == 6 and "3" * 2 == "33"
for text, kind in [("3", int), ('"3"', str), ('"three"', str)]:
    assert type(json.loads('{"quantity": %s}' % text)["quantity"]) is kind
schema = {"order_id": (int, float), "product": str, "quantity": (int, float)}
def ok(rec):
    return set(rec) == set(schema) and all(isinstance(rec[k], t) and not isinstance(rec[k], bool) for k, t in schema.items())
base = {"order_id": 104, "product": "dhokla"}
assert ok({**base, "quantity": 3})
assert not ok({**base, "quantity": "3"})
assert not ok({**base, "quantity": "three"})
assert int("3") == 3
try:
    int("three"); assert False
except ValueError:
    pass
# source: https://json-schema.org/understanding-json-schema/reference/type
#   confirmed: the type keyword specifies the data type a schema should expect, with types like number and string
# source: https://en.wikipedia.org/wiki/JSON_Schema
#   confirmed: "It is specified in an Internet Draft at the IETF"
print("076 ok")
