# checks for notes/164-fan-out-when-a-join-multiplies-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT o.order_id, o.status, oi.product_id FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.order_id IN (104, 105) ORDER BY o.order_id, oi.product_id") == [(104, 'cancelled', 1), (105, 'delivered', 3), (105, 'delivered', 4), (105, 'delivered', 5)]
per = q("SELECT o.order_id, count(*) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id GROUP BY o.order_id ORDER BY 1")
assert per == [(101, 2), (102, 2), (103, 2), (104, 1), (105, 3), (106, 1), (107, 2)]
assert 2 + 2 + 2 + 1 + 3 + 1 + 2 == 13 == sum(n for _, n in per)
assert 13 - 7 == 6 and q("SELECT count(*) FROM orders") == [(7,)]
# every order has at least one item, and an order with none would not appear in the inner join
assert q("SELECT count(*) FROM orders WHERE order_id NOT IN (SELECT order_id FROM order_items)") == [(0,)]
assert q("SELECT c.name, count(*) FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE c.name IN ('Asha', 'Esha') GROUP BY c.name") == [('Asha', 3)]
assert q("SELECT count(*), count(DISTINCT o.order_id) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id") == [(13, 7)]
