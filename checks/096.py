# checks for notes/096-why-many-to-many-cant-live-in-either-table.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
by_order, by_product = {}, {}
for o, p in con.execute("SELECT order_id, product_id FROM order_items ORDER BY 1, 2").fetchall():
    by_order.setdefault(o, []).append(p)
    by_product.setdefault(p, []).append(o)
assert by_order[101] == [1, 5]
assert sorted(by_order[105]) == [3, 4, 5]
assert by_product[1] == [101, 104, 107]
assert by_product[5] == [101, 103, 105]
names = dict(con.execute("SELECT product_id, name FROM products").fetchall())
assert names[1] == "dhokla" and names[5] == "masala chai" and names[4] == "kaju katli" and names[3] == "jalebi"
assert con.execute("SELECT count(*) FROM order_items").fetchone()[0] == 13
# both sides are many: some order has 2 or more products, some product is on 2 or more orders
assert max(len(v) for v in by_order.values()) >= 2 and max(len(v) for v in by_product.values()) >= 2
# repeating order 101 once per product repeats the order_id, which a primary key refuses
con.execute("CREATE TABLE o2 (order_id INTEGER PRIMARY KEY, product_id INTEGER)")
con.execute("INSERT INTO o2 VALUES (101, 1)")
try:
    con.execute("INSERT INTO o2 VALUES (101, 5)")
    raise SystemExit("expected a primary key refusal")
except Exception as e:
    assert "onstraint" in str(e) or "duplicate" in str(e).lower()
# source: https://learn.microsoft.com/en-us/ef/core/modeling/relationships/many-to-many
# confirmed: many-to-many "cannot be represented in a simple way using just a foreign key. Instead, an additional entity type is needed to join the two sides", mapped to a join table
print("096 ok")
