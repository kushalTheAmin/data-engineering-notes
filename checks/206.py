# checks for notes/206-practice-ten-interview-style-sql-questions-on-the-shop.md
import os, sys
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# opening: 6 products, an inner join shows only the 5 that were ordered
assert q("SELECT count(*) FROM products") == [(6,)]
assert q("SELECT count(DISTINCT p.name) FROM products p JOIN order_items oi ON p.product_id = oi.product_id") == [(5,)]
# worked example
assert q("SELECT count(*) FROM orders WHERE status <> 'delivered'") == [(2,)]
assert q("SELECT order_id FROM orders WHERE status <> 'delivered' ORDER BY 1") == [(104,), (106,)]
assert q("SELECT status FROM orders WHERE order_id IN (104, 106) ORDER BY order_id") == [("cancelled",), ("pending",)]
# tasks
assert q("SELECT count(*) AS delivered FROM orders WHERE status = 'delivered'") == [(5,)]
assert q("SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL") == [("Esha",)]
assert q("SELECT p.name, coalesce(sum(oi.quantity), 0) AS units FROM products p LEFT JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.name ORDER BY units DESC, p.name") == [("dhokla", 6), ("jalebi", 4), ("masala chai", 4), ("kaju katli", 3), ("khandvi", 3), ("fafda", 0)]
assert q("SELECT name FROM products WHERE price = (SELECT max(price) FROM products WHERE price < (SELECT max(price) FROM products))") == [("khandvi",)]
assert q("SELECT c.name, count(*) FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name HAVING count(*) > 1 ORDER BY 1") == [("Asha", 3), ("Bhavin", 2)]
assert q("SELECT count(*) FROM products WHERE category = 'sweet' AND category = 'snack'") == [(0,)]
assert q("WITH bought AS (SELECT c.name, p.category FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id) SELECT name FROM bought WHERE category = 'sweet' INTERSECT SELECT name FROM bought WHERE category = 'snack'") == [("Bhavin",)]
assert q('SELECT name, order_id FROM (SELECT c.name, o.order_id, row_number() OVER (PARTITION BY c.name ORDER BY o.ordered_at DESC) AS rn FROM customers c JOIN orders o ON c.customer_id = o.customer_id) WHERE rn = 1 ORDER BY name') == [("Asha", 106), ("Bhavin", 107), ("Chirag", 104), ("Disha", 105)]
assert q("SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status <> 'delivered') ORDER BY c.name") == [("Bhavin",), ("Disha",)]
assert q("SELECT count(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status <> 'delivered')") == [(3,)]
# avg order value: 7 order totals average 18.07, the 13 item lines average 9.73
assert q('WITH t AS (SELECT o.order_id, sum(oi.quantity * p.price) AS total FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.order_id) SELECT round(avg(total), 2) AS avg_order FROM t') == [(18.07,)]
totals = [D("18.00"), D("17.00"), D("10.50"), D("18.00"), D("37.00"), D("15.00"), D("11.00")]
assert q("SELECT round(avg(oi.quantity * p.price), 2) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id") == [(9.73,)]
assert round(sum(totals) / 7, 2) == D("18.07") and round(sum(totals) / 13, 2) == D("9.73")
assert q('WITH t AS (SELECT o.order_id, sum(oi.quantity * p.price) AS total FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.order_id) SELECT order_id, total, sum(total) OVER (ORDER BY order_id) AS running FROM t ORDER BY order_id') == [(101, D("18.00"), D("18.00")), (102, D("17.00"), D("35.00")), (103, D("10.50"), D("45.50")), (104, D("18.00"), D("63.50")), (105, D("37.00"), D("100.50")), (106, D("15.00"), D("115.50")), (107, D("11.00"), D("126.50"))]
# source: https://datalemur.com
# confirmed: page title "DataLemur - Ace the SQL & Data Science Interview", so it offers SQL interview questions
# source: https://www.stratascratch.com
# confirmed: page title "Data Science & AI Interview Prep | StrataScratch" and it lists SQL, so it offers SQL interview questions
# fafda has no order lines, so its sum is NULL and coalesce makes it 0
assert q("SELECT sum(oi.quantity) FROM products p LEFT JOIN order_items oi ON p.product_id = oi.product_id WHERE p.name = 'fafda'") == [(None,)]
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: table 9.1 lists <> as "Not equal" (and != as an alias)
