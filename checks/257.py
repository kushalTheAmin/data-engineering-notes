# checks for notes/257-normal-forms-the-rules-behind-splitting-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# dhokla (product 1) sits on 3 order lines: orders 101, 104, 107
assert q("SELECT count(*) FROM order_items WHERE product_id = 1") == [(3,)]
# Jersey City orders: Asha has 3, Chirag 1, so 4 order rows would carry the copied city
assert q("SELECT count(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'") == [(4,)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)] and q("SELECT count(*) FROM orders WHERE customer_id = 3") == [(1,)]
# order_items key is the pair (order_id, product_id): the row (101, 1, 2) exists
assert q("SELECT order_id, product_id, quantity FROM order_items WHERE order_id = 101 AND product_id = 1") == [(101, 1, 2)]
assert q("SELECT name FROM products WHERE product_id = 1") == [('dhokla',)]
assert q("SELECT tags FROM product_tags WHERE product_id = 1") == [(['steamed', 'savory'],)]
# source: https://en.wikipedia.org/wiki/Database_normalization
# confirmed: Codd introduced 1NF in 1970 and defined 2NF and 3NF in 1971; higher forms exist (BCNF 1974, 4NF, 5NF); a higher level cannot be achieved unless the previous levels are satisfied
