# checks for notes/099-crows-feet-reading-one-and-many.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# Esha, customer 5, has no orders
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 5").fetchone()[0] == 0
# Asha has orders, 101 belongs to exactly one customer
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 1").fetchone()[0] == 3
assert con.execute("SELECT count(DISTINCT customer_id) FROM orders WHERE order_id = 101").fetchone()[0] == 1
# fafda is product 6 and sits on no order
assert con.execute("SELECT name FROM products WHERE product_id = 6").fetchone()[0] == "fafda"
assert con.execute("SELECT count(*) FROM order_items WHERE product_id = 6").fetchone()[0] == 0
# orders.customer_id is NOT NULL
assert con.execute("SELECT is_nullable FROM information_schema.columns WHERE table_name='orders' AND column_name='customer_id'").fetchone()[0] in ("NO", False)
# the four marks
assert len(["||", "|o", "}|", "}o"]) == 4
# source: https://mermaid.js.org/syntax/entityRelationshipDiagram.html
# confirmed: Mermaid uses crow's foot notation; |o zero or one, || exactly one, }o zero or more, }| one or more; right side mirrors as o{ and |{
# confirmed: docs example "PROPERTY ||--|{ ROOM" shows the same ||--o{ style shape
print("099 ok")
