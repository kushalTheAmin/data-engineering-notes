# checks for notes/167-anti-join-rows-with-no-match.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL") == [("Esha", None)]
# the left join makes 8 rows and only Esha has a NULL order_id
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id") == [(8,)]
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL") == [(1,)]
assert q("SELECT p.name FROM products p LEFT JOIN order_items i ON p.product_id = i.product_id WHERE i.product_id IS NULL") == [("fafda",)]
# order_id is the primary key of orders, so it is never NULL in a real row
assert q("SELECT count(*) FROM orders WHERE order_id IS NULL") == [(0,)]
# check yourself 1: Chirag's only order is cancelled
assert q("SELECT status FROM orders WHERE customer_id = 3") == [("cancelled",)]
assert q("SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' WHERE o.order_id IS NULL ORDER BY c.name") == [("Chirag",), ("Esha",)]
# check yourself 2: flipped tables, every order has a customer
assert q("SELECT count(*) FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id WHERE c.customer_id IS NULL") == [(0,)]
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is "a popular Indian snack native to the western state of Gujarat", dough deep-fried till crispy
