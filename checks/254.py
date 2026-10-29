# checks for notes/254-modeling-deciding-the-tables-before-writing-them.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT name FROM customers WHERE customer_id = 1")[0][0] == 'Asha'
assert str(q("SELECT ordered_at FROM orders WHERE order_id = 101")[0][0]) == '2026-04-01 09:15:00'
assert q("SELECT customer_id FROM orders WHERE order_id = 101")[0][0] == 1
assert q("SELECT name, price FROM products WHERE product_id = 1")[0] == ('dhokla', __import__('decimal').Decimal('6.00'))
# order 101 holds two products (dhokla and masala chai), each with quantity 2
assert q("SELECT product_id, quantity FROM order_items WHERE order_id = 101 ORDER BY 1") == [(1, 2), (5, 2)]
assert q("SELECT name FROM products WHERE product_id = 5")[0][0] == 'masala chai'
# dhokla sits in 3 orders
assert q("SELECT count(DISTINCT order_id) FROM order_items WHERE product_id = 1")[0][0] == 3
# order_items has no price column, so old orders are read at the products price
assert 'price' not in [r[0] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'order_items'")]
# five facts in the table
assert 5 == len(["Asha", "2026-04-01 09:15", "dhokla", "6.00", "2"])
# an order holds products at different prices, so a per day price belongs on the order_items row, not on orders
assert q("SELECT count(DISTINCT p.price) FROM order_items i JOIN products p ON p.product_id = i.product_id WHERE i.order_id = 101")[0][0] == 2
assert 'price' not in [r[0] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'orders'")]
