# checks for notes/154-capstone-orders-per-customer-traced-from-rows-to-groups.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM customers") == [(5,)]
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT customer_id, name FROM customers WHERE customer_id <= 4 ORDER BY 1") == [(1, 'Asha'), (2, 'Bhavin'), (3, 'Chirag'), (4, 'Disha')]
assert q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
assert q("SELECT customer_id FROM orders GROUP BY customer_id ORDER BY 1") == [(1,), (2,), (3,), (4,)]
ids = {c: [o for o, cc in q("SELECT order_id, customer_id FROM orders ORDER BY 1") if cc == c] for c in range(1, 6)}
assert ids == {1: [101, 103, 106], 2: [102, 107], 3: [104], 4: [105], 5: []}
rows = q("SELECT customer_id, count(*), sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END), strftime(max(ordered_at), '%m-%d') FROM orders GROUP BY customer_id ORDER BY 1")
assert rows == [(1, 3, 2, '04-08'), (2, 2, 2, '04-09'), (3, 1, 0, '04-04'), (4, 1, 1, '04-06')]
# check yourself 1
assert q("SELECT sum(quantity), count(DISTINCT order_id), count(*) FROM order_items") == [(20, 7, 13)]
assert round(20 / 7, 2) == 2.86 and round(20 / 13, 2) == 1.54
# check yourself 2
assert q("SELECT count(DISTINCT customer_id) FROM orders") == [(4,)]
assert q("SELECT customer_id FROM orders GROUP BY customer_id HAVING count(*) >= 0 ORDER BY 1") == [(1,), (2,), (3,), (4,)]
# Postgres divides two integers as integer division, so 20 / 7 is 2 there; DuckDB / and sqlite show both sides
assert q("SELECT 20 // 7, 20 / 7 > 2.8") == [(2, True)]
# source: https://www.postgresql.org/docs/current/functions-math.html
# confirmed: "Division (for integral types, division truncates the result towards zero)", 5 / 2 gives 2
