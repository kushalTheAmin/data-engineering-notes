# checks for notes/163-joining-three-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
chain = q("SELECT o.order_id, o.status, p.name, oi.quantity FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE o.order_id IN (101, 106) ORDER BY o.order_id, p.name")
assert chain == [(101, 'delivered', 'dhokla', 2), (101, 'delivered', 'masala chai', 2), (106, 'pending', 'khandvi', 2)]
# order 101 has two order_items rows, product 1 and 5
assert q("SELECT product_id FROM order_items WHERE order_id = 101 ORDER BY 1") == [(1,), (5,)]
assert q("SELECT order_id, product_id, quantity FROM order_items WHERE order_id = 101 AND product_id = 1") == [(101, 1, 2)]
assert q("SELECT name FROM products WHERE product_id = 1") == [('dhokla',)]
# 13 rows for all orders, 7 orders, 13 - 7 = 6
n = q("SELECT count(*) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id")
assert n == [(13,)] and q("SELECT count(*) FROM order_items") == [(13,)] and q("SELECT count(*) FROM orders") == [(7,)]
assert 13 - 7 == 6
# reordered joins with fixed ON lines give the same rows
other = q("SELECT o.order_id, o.status, p.name, oi.quantity FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE o.order_id IN (101, 106) ORDER BY o.order_id, p.name")
swapped = q("SELECT o.order_id, o.status, p.name, oi.quantity FROM products p JOIN order_items oi ON oi.product_id = p.product_id JOIN orders o ON o.order_id = oi.order_id WHERE o.order_id IN (101, 106) ORDER BY o.order_id, p.name")
assert other == swapped
# the swapped version with old ON lines fails naming oi
try:
    con.execute("SELECT o.order_id, p.name FROM orders o JOIN products p ON oi.product_id = p.product_id JOIN order_items oi ON o.order_id = oi.order_id")
    assert False
except Exception as e:
    assert 'oi' in str(e) and 'not found' in str(e)
# dhokla is a steamed savory cake, a food description, nothing to compute
# 097: order_items has a composite key of order_id and product_id, one row per pair
assert q("SELECT count(*) FROM (SELECT order_id, product_id FROM order_items GROUP BY 1,2)") == [(13,)]
