# checks for notes/171-joins-plus-group-by-revenue-per-customer.md
import os, sys
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
chain = "FROM customers c {j} orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id"
allrev = q("SELECT c.name, sum(oi.quantity * p.price) " + chain.format(j="JOIN") + " GROUP BY c.name ORDER BY 1")
assert allrev == [("Asha", D("43.50")), ("Bhavin", D("28.00")), ("Chirag", D("18.00")), ("Disha", D("37.00"))]
# asha's 5 joined rows: order 101 (2 dhokla at 6.00, 2 chai at 3.00), 103 (khandvi 7.50, chai 3.00), 106 (2 khandvi at 7.50)
assert [2 * 6, 2 * 3, 1 * 7.5, 1 * 3, 2 * 7.5] == [12, 6, 7.5, 3, 15] and sum([12, 6, 7.5, 3, 15]) == 43.5
assert q("SELECT count(*) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.customer_id = 1") == [(5,)]
# chirag only has order 104, cancelled
assert q("SELECT order_id, status FROM orders WHERE customer_id = 3") == [(104, "cancelled")]
assert q("SELECT count(*) FROM orders WHERE customer_id = 3 AND status = 'delivered'") == [(0,)]
dl = q("SELECT c.name, sum(oi.quantity * p.price) " + chain.format(j="JOIN") + " WHERE o.status = 'delivered' GROUP BY c.name ORDER BY 1")
assert dl == [("Asha", D("28.50")), ("Bhavin", D("28.00")), ("Disha", D("37.00"))]
assert q("SELECT status, order_id FROM orders WHERE order_id = 106") == [("pending", 106)]
assert D("43.50") - D("15.00") == D("28.50")
# esha has no orders, so the inner join drops her
assert q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
cat = q("SELECT p.category, sum(oi.quantity * p.price) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY p.category ORDER BY 1")
assert cat == [("drink", D("12.00")), ("snack", D("58.50")), ("sweet", D("56.00"))]
assert sum(r[1] for r in cat) == D("126.50") == sum(r[1] for r in allrev)
assert q("SELECT category FROM products ORDER BY price DESC LIMIT 1") == [("sweet",)]
left_then_inner = q("SELECT c.name, sum(oi.quantity * p.price) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY 1")
assert len(left_then_inner) == 4 and "Esha" not in [r[0] for r in left_then_inner]
assert q("SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE c.customer_id = 5") == [("Esha", None)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: JOIN is inner by default and LEFT OUTER JOIN keeps unmatched left rows, filled in with null
assert q("SELECT sum(revenue) FROM (SELECT p.category, sum(oi.quantity * p.price) AS revenue FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY p.category)") == [(D("126.50"),)]
assert q("SELECT count(*) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id") == [(13,)]
