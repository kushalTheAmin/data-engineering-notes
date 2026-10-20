# checks for notes/106-where-keeping-only-the-rows-that-match.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT order_id, customer_id, status FROM orders ORDER BY order_id").fetchall()
assert len(rows) == 7
kept = [r[0] for r in rows if r[2] == "delivered"]
assert kept == [101, 102, 103, 105, 107]
assert [r[0] for r in rows if r[2] != "delivered"] == [104, 106]
assert [r[2] for r in rows if r[0] in (104, 106)] == ["cancelled", "pending"]
assert con.execute("SELECT order_id FROM orders WHERE status = 'delivered'").fetchall() == [(i,) for i in kept]
# filter on a column not selected
assert con.execute("SELECT order_id FROM orders WHERE status = 'delivered'").description[0][0] == "order_id"
# exact text match
assert con.execute("SELECT order_id FROM orders WHERE status = 'Delivered'").fetchall() == []
assert con.execute("SELECT name FROM products WHERE category = 'Snack'").fetchall() == []
assert con.execute("SELECT count(*) FROM products WHERE category = 'snack'").fetchone()[0] == 3
cust = [r[0] for r in con.execute("SELECT customer_id FROM orders WHERE status = 'delivered' ORDER BY order_id").fetchall()]
assert cust == [1, 2, 1, 4, 2] and len(cust) == 5 and len(set(cust)) == 3
# source: https://duckdb.org/docs/current/sql/query_syntax/where
# confirmed: WHERE specifies filters to apply to the data, and logically it is applied immediately after the FROM clause
# source: https://dev.mysql.com/doc/refman/8.4/en/case-sensitivity.html
# confirmed: "nonbinary string comparisons are case-insensitive by default" in MySQL, so the exact match claim is DuckDB only
print("106 ok")
