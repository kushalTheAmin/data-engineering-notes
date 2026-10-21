# checks for notes/141-what-nulls-do-to-sum-and-avg.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT order_id, stars FROM order_ratings ORDER BY order_id")
assert rows == [(101, 5), (102, 4), (103, None), (105, 3), (107, None)]
total = count = 0
trace = []
for _, v in rows:
    if v is not None:
        total += v
        count += 1
    trace.append((total, count))
assert trace == [(5, 1), (9, 2), (9, 2), (12, 3), (12, 3)]
assert total / count == 4.0 and total / len(rows) == 2.4
assert q("SELECT sum(stars), count(stars), count(*), avg(stars), sum(stars) * 1.0 / count(*) FROM order_ratings") == [(12, 3, 5, 4.0, 2.4)]
assert q("SELECT sum(stars), avg(stars), count(*) FROM order_ratings WHERE stars IS NULL") == [(None, None, 2)]
assert q("SELECT sum(stars), avg(stars), sum(stars) * 1.0 / count(*) FROM order_ratings WHERE order_id >= 103") == [(3, 3.0, 1.0)]
assert 3 / 3 == 1.0 and 3 / 1 == 3.0
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: avg is "the average (arithmetic mean) of all the non-null input values", sum is "the sum of the non-null input values"
