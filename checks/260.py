# checks for notes/260-second-normal-form-nothing-about-half-the-key.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# dhokla is on 3 order lines: 101 (2), 104 (3), 107 (1)
assert q("SELECT oi.order_id, oi.quantity FROM order_items oi WHERE oi.product_id = 1 ORDER BY 1") == [(101, 2), (104, 3), (107, 1)]
assert q("SELECT count(*) FROM order_items WHERE product_id = 1") == [(3,)]
# the key is the pair: product 1 alone gives 3 different quantities
assert q("SELECT count(DISTINCT quantity) FROM order_items WHERE product_id = 1") == [(3,)]
# product_id alone decides name
assert q("SELECT count(*) FROM (SELECT product_id FROM products GROUP BY product_id HAVING count(DISTINCT name) > 1)") == [(0,)]
# kaju katli (4) is on orders 102 and 105
assert q("SELECT order_id FROM order_items WHERE product_id = 4 ORDER BY 1") == [(102,), (105,)]
# order 105 has 3 lines
assert q("SELECT count(*) FROM order_items WHERE order_id = 105") == [(3,)]
# source: https://en.wikipedia.org/wiki/Database_normalization
# confirmed: second normal form, non-key attributes must depend on the "whole candidate key, not just part of it", violations involve a composite key
