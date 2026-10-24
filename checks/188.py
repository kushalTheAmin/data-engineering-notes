# checks for notes/188-rank-vs-dense-rank-what-ties-do.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the slice: orders 102 and 105, quantity biggest first
items = q("SELECT order_id, product_id, quantity FROM order_items WHERE order_id IN (102, 105)")
assert sorted(items) == [(102, 3, 1), (102, 4, 1), (105, 3, 2), (105, 4, 2), (105, 5, 1)]
qs = [r[2] for r in items]
# rank = 1 + rows strictly ahead; dense_rank = 1 + distinct values ahead
rk = lambda v: 1 + sum(1 for x in qs if x > v)
dr = lambda v: 1 + len({x for x in qs if x > v})
assert (rk(2), rk(1)) == (1, 3)
assert (dr(2), dr(1)) == (1, 2)
got = q("SELECT order_id, product_id, quantity, rank() OVER (ORDER BY quantity DESC) AS rk, dense_rank() OVER (ORDER BY quantity DESC) AS dr FROM order_items WHERE order_id IN (102, 105) ORDER BY quantity DESC, order_id, product_id")
assert got == [(105, 3, 2, 1, 1), (105, 4, 2, 1, 1), (102, 3, 1, 3, 2), (102, 4, 1, 3, 2), (105, 5, 1, 3, 2)]
# top N: rk <= 2 keeps 2 rows, dr <= 2 keeps all 5
assert sum(1 for r in got if r[3] <= 2) == 2
assert sum(1 for r in got if r[4] <= 2) == 5
assert len({r[2] for r in got}) == 2
# whole table: 1 + 5 + 7 = 13 rows, quantity 1 ranks 1 + 5 + 1 = 7th
assert q("SELECT quantity, count(*) FROM order_items GROUP BY quantity ORDER BY quantity DESC") == [(3, 1), (2, 5), (1, 7)]
assert 1 + 5 + 7 == 13
assert 1 + 5 + 1 == 7
assert q("SELECT DISTINCT quantity, rank() OVER (ORDER BY quantity DESC) AS rk FROM order_items ORDER BY quantity DESC") == [(3, 1), (2, 2), (1, 7)]
# source: https://www.postgresql.org/docs/current/functions-window.html
# confirmed: rank() is "the row_number of the first row in its peer group", with gaps; dense_rank() is without gaps and counts peer groups
