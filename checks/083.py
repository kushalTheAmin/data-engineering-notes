# checks for notes/083-schema-on-write-vs-schema-on-read.md
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT quantity FROM order_items WHERE order_id=104 AND product_id=1").fetchone()[0] == 3
assert con.execute("SELECT name FROM products WHERE product_id=1").fetchone()[0] == "dhokla"
assert con.execute("SELECT quantity FROM order_items WHERE order_id=105 AND product_id=4").fetchone()[0] == 2
lines = ['{"order_id": 104, "quantity": 3}', '{"order_id": 105, "quantity": "two"}']
try:
    sum(json.loads(l)["quantity"] for l in lines)
    raise SystemExit("should have failed")
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for +: 'int' and 'str'"
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 105").fetchone()[0] == 3
total = con.execute("SELECT sum(quantity) FROM order_items WHERE order_id = 105").fetchone()[0]
assert total == 5 and total - 2 == 3
# source: https://www.mongodb.com/docs/manual/core/schema-validation/
#   confirmed: "MongoDB uses a flexible schema model. By default, documents in a collection don't need the same fields or data types"
# source: https://www.sqlite.org/stricttables.html
#   confirmed: "SQLite strives to be flexible regarding the datatype of the content that it stores"
print("083 ok")
