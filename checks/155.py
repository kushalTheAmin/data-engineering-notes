# checks for notes/155-why-joins-the-answer-lives-in-more-than-one-table.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT customer_id FROM orders WHERE order_id = 104") == [(3,)]
assert q("SELECT name, city FROM customers WHERE customer_id = 3") == [('Chirag', 'Jersey City')]
assert q("SELECT status FROM orders WHERE order_id = 104") == [('cancelled',)]
assert q("SELECT order_id, customer_id FROM orders WHERE order_id IN (101, 104, 105) ORDER BY 1") == [(101, 1), (104, 3), (105, 4)]
assert q("SELECT customer_id, name, city FROM customers WHERE customer_id IN (1, 3, 4) ORDER BY 1") == [(1, 'Asha', 'Jersey City'), (3, 'Chirag', 'Jersey City'), (4, 'Disha', 'Hoboken')]
r = q("SELECT orders.order_id, customers.name, customers.city FROM orders JOIN customers ON orders.customer_id = customers.customer_id ORDER BY orders.order_id")
assert len(r) == 7 == q("SELECT count(*) FROM orders")[0][0]
assert q("SELECT count(*) FROM customers") == [(5,)]
assert 'Esha' not in [x[1] for x in r]
assert q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
# source: https://www.postgresql.org/docs/current/planner-optimizer.html
# confirmed: the docs name the nested loop join, where the right relation is scanned once for every row of the left, and also list merge and hash joins
