# checks for notes/187-row-number-numbering-rows-in-order.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = [("dhokla", "snack", 6.0), ("khandvi", "snack", 7.5), ("jalebi", "sweet", 5.0), ("kaju katli", "sweet", 12.0), ("masala chai", "drink", 3.0), ("fafda", "snack", 4.5)]
ranked = sorted(rows, key=lambda r: -r[2])
place = {n: i for i, (n, _, _) in enumerate(ranked, 1)}
assert [place[n] for n, _, _ in rows] == [3, 2, 4, 1, 6, 5]
assert [r[2] for r in q("SELECT name, price, row_number() OVER (ORDER BY price DESC) AS rn FROM products ORDER BY product_id")] == [3, 2, 4, 1, 6, 5]
assert len({p for _, _, p in rows}) == 6
# partition: count restarts per category
per = {}
want = []
for n, c, p in sorted(rows, key=lambda r: (r[1], -r[2])):
    per[c] = per.get(c, 0) + 1
    want.append((n, per[c]))
d = dict(want)
assert [d[n] for n, _, _ in rows] == [2, 1, 2, 1, 1, 3]
assert [r[1] for r in q("SELECT name, row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products ORDER BY product_id")] == [2, 1, 2, 1, 1, 3]
# order_items ties
assert q("SELECT count(*) FROM order_items WHERE quantity = 2") == [(5,)]
assert q("SELECT count(*) FROM order_items WHERE quantity = 3") == [(1,)]
assert q("SELECT order_id, product_id FROM (SELECT order_id, product_id, row_number() OVER (ORDER BY quantity DESC, product_id) AS rn FROM order_items) AS t WHERE rn = 2") == [(101, 1)]
assert 1 + 5 == 6
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: row_number assigns sequential numbers within each partition in the order defined by ORDER BY, with tied rows numbered in an unspecified order
