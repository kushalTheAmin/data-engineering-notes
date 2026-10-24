# checks for notes/185-over-the-window-a-function-looks-through.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = [("dhokla", 6.0), ("khandvi", 7.5), ("jalebi", 5.0), ("kaju katli", 12.0), ("masala chai", 3.0), ("fafda", 4.5)]
assert len(rows) == 6
assert q("SELECT count(*) FROM products") == [(6,)]
out = []
for name, price in rows:
    window = rows
    avg = sum(p for _, p in window) / len(window)
    out.append((name, price, round(price - avg, 2)))
assert out == [("dhokla", 6.0, -0.33), ("khandvi", 7.5, 1.17), ("jalebi", 5.0, -1.33), ("kaju katli", 12.0, 5.67), ("masala chai", 3.0, -3.33), ("fafda", 4.5, -1.83)]
sql = q("SELECT name, price, round(price - avg(price) OVER (), 2) AS vs_avg FROM products ORDER BY product_id")
assert [(n, float(p), v) for n, p, v in sql] == out
assert round(38 / 6, 2) == 6.33
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# source: https://www.postgresql.org/docs/current/functions-window.html
# confirmed: any built-in or user-defined ordinary aggregate can be used as a window function, so a window function is not always an aggregate
# confirmed: a window function performs a calculation across rows related to the current row, a window function call always contains an OVER clause, rows keep their separate identities, and with no PARTITION BY the window is the whole table
