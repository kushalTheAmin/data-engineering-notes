# checks for notes/151-pivoting-turning-rows-into-columns.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the long shape, 5 rows, slice shows rows 1, 2 and 4
long_rows = q("SELECT customer_id, status, count(*) FROM orders GROUP BY customer_id, status ORDER BY customer_id, status")
assert len(long_rows) == 5
assert long_rows[0] == (1, 'delivered', 2) and long_rows[1] == (1, 'pending', 1) and long_rows[3] == (3, 'cancelled', 1)
assert q("SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END), sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END), sum(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) FROM orders GROUP BY customer_id ORDER BY customer_id") == [(1, 2, 1, 0), (2, 2, 0, 0), (3, 0, 0, 1), (4, 1, 0, 0)]
assert q("SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END), sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END), count(*) FROM orders GROUP BY customer_id ORDER BY customer_id") == [(1, 2, 1, 3), (2, 2, 0, 2), (3, 0, 0, 1), (4, 1, 0, 1)]
# DuckDB PIVOT gives the same wide shape
assert q("PIVOT orders ON status USING count(*) GROUP BY customer_id ORDER BY customer_id") == [(1, 0, 2, 1), (2, 0, 2, 0), (3, 1, 0, 0), (4, 0, 1, 0)]
# source: https://duckdb.org/docs/2.0/sql/statements/pivot.html
# confirmed: "The PIVOT statement allows distinct values within a column to be separated into their own columns" and a simplified syntax "that automatically detects the columns to create"
# customer 2 has no cancelled order, so 144 had no row for the pair and the wide table shows 0
assert (2, 'cancelled') not in [(r[0], r[1]) for r in long_rows]
