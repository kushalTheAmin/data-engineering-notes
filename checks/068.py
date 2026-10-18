# checks for notes/068-nesting.md
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT count(*) FROM order_items").fetchone()[0] == 13
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 103").fetchone()[0] == 2
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 105").fetchone()[0] == 3
assert con.execute("SELECT string_agg(p.name || ':' || i.quantity, ',' ORDER BY p.product_id) FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 103").fetchone()[0] == "khandvi:1,masala chai:1"
assert con.execute("SELECT c.name, c.city FROM orders o JOIN customers c USING (customer_id) WHERE o.order_id = 103").fetchall() == [("Asha", "Jersey City")]
d = json.loads('{"order_id": 103, "customer": {"name": "Asha", "city": "Jersey City"}, "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]}')
assert d["items"][1]["product"] == "masala chai" and len(d["items"]) == 2
try:
    d["items"][2]
    raise SystemExit("should fail")
except IndexError:
    pass
# source: https://www.rfc-editor.org/rfc/rfc8259
#   confirmed: "An implementation may set limits on the maximum depth of nesting"
print("068 ok")
