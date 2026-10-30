# checks for notes/269-big-o-in-plain-words-how-work-grows-as-data-grows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
q = lambda con, s: con.execute(s).fetchall()

def find(rows, wanted):
    steps = 0
    for row in rows:
        steps += 1
        if row["customer_id"] == wanted:
            break
    return steps

# first costs 1 at any size, last and missing cost n, so doubling rows doubles steps
for n in (1000, 2000, 4000):
    reviews = [{"customer_id": i, "rating": 5} for i in range(1, n + 1)]
    assert (find(reviews, 1), find(reviews, n), find(reviews, 0)) == (1, n, n)
# check yourself 1: missing customer over 500 and 5000 rows
for n in (500, 5000):
    assert find([{"customer_id": i} for i in range(1, n + 1)], 0) == n
# check yourself 2: the shop has 13 order_items, (105, 4) is the 9th in sorted order
con = shop()
assert q(con, "SELECT count(*) FROM order_items") == [(13,)]
assert q(con, "SELECT n FROM (SELECT order_id, product_id, row_number() OVER (ORDER BY order_id, product_id) AS n FROM order_items) WHERE order_id = 105 AND product_id = 4") == [(9,)]
# 4 reviews in the 268 reviews table, 4 million in the hook is just the scenario
# source: https://www.postgresql.org/docs/current/indexes-intro.html
#  opened this run: "With no advance preparation, the system would have to scan the entire test1 table, row by row, to find all matching entries"
