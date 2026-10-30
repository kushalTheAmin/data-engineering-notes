# checks for notes/272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def nested(outer, inner):
    steps = 0
    for a in outer:
        for b in inner:
            steps += 1
    return steps

# the shop has orders 101 to 107, 6 products with ids 1 to 6, 5 customers
assert [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()] == list(range(101, 108))
assert [r[0] for r in con.execute("SELECT product_id FROM products ORDER BY 1").fetchall()] == [1, 2, 3, 4, 5, 6]
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
product_ids = [1, 2, 3, 4, 5, 6]
for n, a, b in [(7, 42, 49), (70, 420, 4900), (700, 4200, 490000)]:
    order_ids = list(range(101, 101 + n))
    assert nested(order_ids, product_ids) == a == n * 6
    assert nested(order_ids, order_ids) == b == n * n
# question 1
assert 7000 * 6 == 42000
# question 2
assert 5 * 7 == 35 and 500 * 700 == 350000 == 35 * 100 * 100 and 35 * 100 == 3500
# source: https://www.postgresql.org/docs/current/planner-optimizer.html
# confirmed: nested loop join "The right relation is scanned once for every row found in the left relation", and an index scan on the right can make it a good strategy
# also: the same page lists three join strategies (nested loop join, merge join, hash join), so a join is only sometimes this loop
