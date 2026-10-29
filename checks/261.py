# checks for notes/261-third-normal-form-nothing-but-the-key.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT o.order_id, o.customer_id, c.city FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.order_id <= 104 ORDER BY 1") == [(101, 1, 'Jersey City'), (102, 2, 'Edison'), (103, 1, 'Jersey City'), (104, 3, 'Jersey City')]
# Asha (customer 1) has orders 101, 103, 106
assert q("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY 1") == [(101,), (103,), (106,)]
# Jersey City: Asha 3 + Chirag 1 = 4 orders
assert q("SELECT count(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'") == [(4,)]
# order_id decides customer_id, customer_id decides city
assert q("SELECT count(*) FROM (SELECT customer_id FROM customers GROUP BY customer_id HAVING count(DISTINCT city) > 1)") == [(0,)]
assert q("SELECT count(*) FROM (SELECT order_id FROM orders GROUP BY order_id HAVING count(DISTINCT customer_id) > 1)") == [(0,)]
