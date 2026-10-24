# checks for notes/186-partition-by-a-separate-window-per-group.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = [("dhokla", "snack", 6.0), ("khandvi", "snack", 7.5), ("jalebi", "sweet", 5.0), ("kaju katli", "sweet", 12.0), ("masala chai", "drink", 3.0), ("fafda", "snack", 4.5)]
def avg_in(cat):
    ps = [p for _, c, p in rows if c == cat]
    return sum(ps) / len(ps)
assert [avg_in(c) for c in ("snack", "sweet", "drink")] == [6.0, 8.5, 3.0]
sql = q("SELECT name, category, price, avg(price) OVER (PARTITION BY category) AS category_avg FROM products ORDER BY product_id")
assert [(n, c, float(p), a) for n, c, p, a in sql] == [(n, c, p, avg_in(c)) for n, c, p in rows]
assert len(sql) == 6
assert q("SELECT category, avg(price) FROM products GROUP BY category ORDER BY category") == [("drink", 3.0), ("snack", 6.0), ("sweet", 8.5)]
# 177 baton: fafda and jalebi are under their own category average
assert q("SELECT name FROM (SELECT name, price, avg(price) OVER (PARTITION BY category) AS a FROM products) AS t WHERE price < a ORDER BY name") == [("fafda",), ("jalebi",)]
assert 6.0 + 7.5 == 13.5
assert 6.0 + 7.5 + 4.5 == 18.0
assert [float(t) for _, t in q("SELECT name, sum(price) OVER (PARTITION BY category) AS t FROM products WHERE price > 5 ORDER BY product_id")] == [13.5, 13.5, 12.0]
assert all(d == 0 for _, d in q("SELECT name, price - avg(price) OVER (PARTITION BY name) AS d FROM products"))
assert min(p for _, _, p in rows) == 3.0
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: PARTITION BY divides rows into groups sharing the same values, the window function sees only rows in the current row's partition, and unlike GROUP BY every row is kept
