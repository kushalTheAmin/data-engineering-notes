# checks for notes/077-required-vs-optional-fields.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT customer_id, name, city FROM customers WHERE customer_id IN (1, 5) ORDER BY 1").fetchall() == [(1, "Asha", "Jersey City"), (5, "Esha", None)]
assert con.execute("SELECT city FROM customers WHERE customer_id = 2").fetchall() == [("Edison",)]
required = ["customer_id", "name"]
records = [
    {"customer_id": 1, "name": "Asha", "city": "Jersey City"},
    {"customer_id": 5, "name": "Esha"},
    {"customer_id": 2, "city": "Edison"},
]
assert [[n for n in required if n not in r] for r in records] == [[], [], ["name"]]
esha = {"customer_id": 5, "name": "Esha"}
assert esha.get("city") is None
try:
    esha["city"]; assert False
except KeyError:
    pass
withnull = {"order_id": 103, "stars": None}
assert all(n in withnull for n in ["order_id", "stars"])
assert not all(n in {"order_id": 103} for n in ["order_id", "stars"])
assert con.execute("SELECT order_id FROM order_ratings WHERE stars IS NULL ORDER BY 1").fetchall() == [(103,), (107,)]
assert con.execute("SELECT count(*) FROM orders").fetchone()[0] == 7
# source: https://json-schema.org/understanding-json-schema/reference/object
#   confirmed: properties defined by the properties keyword are not required by default; a required list names the required ones
print("077 ok")
