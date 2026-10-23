# checks for notes/184-window-functions-a-total-next-to-every-row.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal as D
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM products") == [(6,)]
rows = q("SELECT name, price, sum(price) OVER () AS total FROM products ORDER BY product_id")
assert len(rows) == 6 and all(r[2] == D("38.00") for r in rows)
assert q("SELECT sum(price) FROM products") == [(D("38.00"),)]
assert len(q("SELECT sum(price) FROM products")) == 1
prices = {"dhokla": 6.0, "khandvi": 7.5, "jalebi": 5.0, "kaju katli": 12.0, "masala chai": 3.0, "fafda": 4.5}
assert sum(prices.values()) == 38.0
assert [(n, float(p)) for n, p, _ in rows] == list(prices.items())
# check yourself 1
assert round(38 / 6, 2) == 6.33
assert q("SELECT round(avg(price), 2) FROM products") == [(6.33,)]
assert q("SELECT name FROM (SELECT name, price, avg(price) OVER () AS a FROM products) AS t WHERE price > a ORDER BY name") == [("kaju katli",), ("khandvi",)]
assert q("SELECT price FROM products WHERE name = 'dhokla'") == [(D("6.00"),)]
# check yourself 2
r2 = q("SELECT name, sum(price) OVER () AS total FROM products WHERE category = 'snack' ORDER BY product_id")
assert r2 == [("dhokla", D("18.00")), ("khandvi", D("18.00")), ("fafda", D("18.00"))]
assert 6 + 7.5 + 4.5 == 18
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: window functions do not group rows into a single output row, rows keep their separate identities; a row removed by WHERE is not seen by any window function; windows run after WHERE, GROUP BY and HAVING
