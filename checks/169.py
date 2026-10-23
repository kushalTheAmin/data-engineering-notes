# checks for notes/169-cross-join-every-row-with-every-row.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the python loop: 2 customers times 3 products
pairs = [(c, p) for c in ["Asha", "Bhavin"] for p in ["dhokla", "khandvi", "jalebi"]]
assert len(pairs) == 6 == 2 * 3
assert q("SELECT count(*), count(DISTINCT c.name), count(DISTINCT p.name) FROM customers c CROSS JOIN products p") == [(30, 5, 6)]
assert 5 * 6 == 30
assert 10000 * 10000 == 100_000_000
# the comma form gives the same 30 rows
assert q("SELECT count(*) FROM customers, products") == [(30,)]
# 10 distinct customer and product pairs were ordered, so 20 never were
ordered = "SELECT DISTINCT o.customer_id, i.product_id FROM orders o JOIN order_items i ON o.order_id = i.order_id"
assert q(f"SELECT count(*) FROM ({ordered})") == [(10,)]
never = q(f"SELECT c.name, count(*) FROM customers c CROSS JOIN products p LEFT JOIN ({ordered}) t ON t.customer_id = c.customer_id AND t.product_id = p.product_id WHERE t.product_id IS NULL GROUP BY c.name ORDER BY c.name")
assert never == [("Asha", 3), ("Bhavin", 3), ("Chirag", 5), ("Disha", 3), ("Esha", 6)]
assert sum(n for _, n in never) == 20 == 30 - 10
assert q("SELECT count(*) FROM products") == [(6,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: a cross join gives every combination of rows, N and M rows give N * M rows, and FROM T1 CROSS JOIN T2 is equivalent to FROM T1, T2 and to INNER JOIN ON TRUE
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model", so Postgres is a server database
