# checks for notes/122-computed-columns-and-as.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
r = con.execute("SELECT name, price - 1 FROM products")
assert [d[0] for d in r.description] == ["name", "(price - 1)"]
assert [x[1] for x in r.fetchall()] == [Decimal(v) for v in ["5.00", "6.50", "4.00", "11.00", "2.00", "3.50"]]
rows = [{"name": n, "price": p} for n, p in q("SELECT name, price FROM products")]
new = [{"name": r["name"], "sale_price": r["price"] - 1} for r in rows]
assert q("SELECT name, price - 1 AS sale_price FROM products ORDER BY sale_price DESC") == [
    (d["name"], d["sale_price"]) for d in sorted(new, key=lambda d: -d["sale_price"])]
assert len(con.execute("SELECT * FROM products").description) == 4
assert q("SELECT price FROM products WHERE name = 'dhokla'")[0][0] == Decimal("6.00")
assert len(q("SELECT name FROM products WHERE price - 1 < 5")) == 3
assert len(q("SELECT name, price - 1 AS sale_price FROM products WHERE sale_price < 5")) == 3
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: output column name can be used in ORDER BY and GROUP BY but not WHERE or HAVING; generated name such as ?column? when none is given
