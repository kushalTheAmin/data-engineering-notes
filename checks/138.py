# checks for notes/138-count-star-vs-count-of-a-column.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT order_id, stars, stars_zero_filled FROM order_ratings ORDER BY order_id")
assert len(rows) == 5
assert sum(1 for r in rows if r[1] is not None) == 3
assert sum(1 for r in rows if r[2] is not None) == 5
assert q("SELECT count(*), count(stars), count(stars_zero_filled) FROM order_ratings") == [(5, 3, 5)]
assert q("SELECT count(*), count(stars) FROM order_ratings WHERE stars IS NULL") == [(2, 0)]
assert q("SELECT count(*), count(stars), count(stars_zero_filled) FROM order_ratings WHERE order_id >= 105") == [(2, 1, 2)]
assert q("SELECT count(stars_zero_filled) * 100.0 / count(*) FROM order_ratings") == [(100.0,)]
assert q("SELECT count(stars) * 100.0 / count(*) FROM order_ratings") == [(60.0,)]
assert 3 * 100.0 / 5 == 60.0
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: count(*) "Computes the number of input rows"; count("any") "Computes the number of input rows in which the input value is not null"
