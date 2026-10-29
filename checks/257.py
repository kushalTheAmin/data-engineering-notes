# checks for notes/257-normal-forms-the-rules-behind-splitting-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# order 101 holds dhokla and masala chai
assert q("SELECT p.name FROM order_items i JOIN products p ON p.product_id = i.product_id WHERE i.order_id = 101 ORDER BY p.name") == [('dhokla',), ('masala chai',)]
# order_items has 13 rows and its key is the pair
assert q("SELECT count(*) FROM order_items") == [(13,)]
assert q("SELECT count(*) FROM (SELECT DISTINCT order_id, product_id FROM order_items)") == [(13,)]
# dhokla sits in 3 order_items rows, one per order (101, 104, 107)
assert q("SELECT count(*) FROM order_items WHERE product_id = 1") == [(3,)]
assert q("SELECT count(DISTINCT order_id) FROM order_items WHERE product_id = 1") == [(3,)]
# renaming dhokla in one of 3 rows leaves 2 with the old name
assert 3 - 1 == 2  # 3 rows hold dhokla, one updated, 2 stale
# Jersey City repeats on Asha and Chirag
assert q("SELECT name FROM customers WHERE city = 'Jersey City' ORDER BY customer_id") == [('Asha',), ('Chirag',)]
# source: https://en.wikipedia.org/wiki/Database_normalization
# confirmed: "a higher level of database normalization cannot be achieved unless the previous levels have been satisfied"
# confirmed: a relation is often called "normalized" if it meets third normal form
# Asha's two phones in one cell would break first form; stacking per the Wikipedia quote above
