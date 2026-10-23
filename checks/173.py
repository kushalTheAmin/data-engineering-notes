# checks for notes/173-capstone-the-shop-revenue-report-from-four-tables.md
import os, sys
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
base = "FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered'"
i2 = base + " LEFT JOIN order_items oi ON o.order_id = oi.order_id"
i3 = i2 + " LEFT JOIN products p ON oi.product_id = p.product_id"
# the row count table
assert q("SELECT count(*) FROM customers") == [(5,)]
assert q("SELECT count(*) " + base) == [(7,)]
assert q("SELECT count(*) " + i2) == [(13,)]
assert q("SELECT count(*) " + i3) == [(13,)]
# the report
assert q("SELECT c.name, count(DISTINCT o.order_id), coalesce(sum(oi.quantity), 0), coalesce(sum(oi.quantity * p.price), 0) " + i3 + " GROUP BY c.name ORDER BY c.name") == [
    ("Asha", 2, 6, D("28.50")), ("Bhavin", 2, 4, D("28.00")), ("Chirag", 0, 0, D("0.00")), ("Disha", 1, 5, D("37.00")), ("Esha", 0, 0, D("0.00"))]
# question 1
assert q("SELECT c.name, count(o.order_id) " + i3 + " GROUP BY c.name ORDER BY c.name") == [("Asha", 4), ("Bhavin", 4), ("Chirag", 0), ("Disha", 3), ("Esha", 0)]
# question 2
assert q("SELECT o.status, sum(oi.quantity * p.price) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.status ORDER BY 1") == [("cancelled", D("18.00")), ("delivered", D("93.50")), ("pending", D("15.00"))]
assert D("28.50") + D("28.00") + D("37.00") == D("93.50") and D("18.00") + D("15.00") == D("33.00") and D("93.50") + D("33.00") == D("126.50")
assert D("43.50") + D("28.00") + D("18.00") + D("37.00") == D("126.50")
# the 13 rows after the order_items join are 11 real items plus a filler row each for chirag and esha
assert q("SELECT count(oi.product_id), count(*) - count(oi.product_id) " + i2) == [(11, 2)]
# the items column adds up quantity: asha has 4 joined rows holding 6 units
assert q("SELECT count(oi.product_id), sum(oi.quantity) " + i2 + " WHERE c.name = 'Asha'") == [(4, 6)]
