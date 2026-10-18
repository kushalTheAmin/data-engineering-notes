# checks for notes/075-schema.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = dict((r[0], r[1:]) for r in con.execute(
    "SELECT o.order_id, c.name, o.status FROM orders o JOIN customers c USING (customer_id)").fetchall())
assert rows[101] == ("Asha", "delivered")
assert rows[104] == ("Chirag", "cancelled")
assert rows[105] == ("Disha", "delivered")
assert con.execute("SELECT note FROM order_notes WHERE order_id = 105").fetchone() == ("gift, please wrap",)
schema = ["order_id", "customer", "status"]
assert len(schema) == 3
records = {
    101: ["order_id", "customer", "status"],
    104: ["order_id", "customer", "state"],
    105: ["order_id", "customer", "status", "gift_wrap"],
}
expect = {101: ([], []), 104: (["status"], ["state"]), 105: ([], ["gift_wrap"])}
for k, names in records.items():
    missing = [n for n in schema if n not in names]
    extra = [n for n in names if n not in schema]
    assert (missing, extra) == expect[k]
import json
json.loads('{"order_id": 104, "customer": "Chirag", "state": "cancelled"}')  # valid JSON, wrong shape
# source: https://json-schema.org/
#   confirmed: JSON Schema is described as the vocabulary that enables JSON data consistency, validity, and interoperability
print("075 ok")
