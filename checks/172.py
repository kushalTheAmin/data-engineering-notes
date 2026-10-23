# checks for notes/172-practice-five-join-questions-on-the-shop-checking-row-counts.md
import os, sys
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the table: rows out for three joins
assert q("SELECT count(*) FROM customers c JOIN orders o ON c.customer_id = o.customer_id") == [(7,)]
assert q("SELECT count(*) FROM orders") == [(7,)] and q("SELECT count(*) FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)") == [(1,)]
assert q("SELECT count(*) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id") == [(13,)]
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id") == [(8,)] and 7 + 1 == 8
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
# task 1: 13 item rows plus Esha, and every order has at least one item
assert q("SELECT count(*) FROM orders WHERE order_id NOT IN (SELECT order_id FROM order_items)") == [(0,)]
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id LEFT JOIN order_items oi ON o.order_id = oi.order_id") == [(14,)] and 13 + 1 == 14
# task 2
assert q("SELECT count(*), count(o.order_id) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id") == [(8, 7)]
# task 3
assert q("SELECT c.name, count(*), count(DISTINCT o.order_id) FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.name ORDER BY 1") == [("Asha", 5, 3), ("Bhavin", 4, 2), ("Chirag", 1, 1), ("Disha", 3, 1)]
assert q("SELECT count(*) FROM order_items WHERE order_id = 105") == [(3,)] and q("SELECT customer_id FROM orders WHERE order_id = 105") == [(4,)]
# task 4
r4 = q("SELECT c.name, coalesce(sum(oi.quantity * p.price), 0) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' LEFT JOIN order_items oi ON o.order_id = oi.order_id LEFT JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY 1")
assert r4 == [("Asha", D("28.50")), ("Bhavin", D("28.00")), ("Chirag", D("0.00")), ("Disha", D("37.00")), ("Esha", D("0.00"))]
w4 = q("SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id LEFT JOIN order_items oi ON o.order_id = oi.order_id LEFT JOIN products p ON oi.product_id = p.product_id WHERE o.status = 'delivered' GROUP BY c.name")
assert len(w4) == 3
# task 5
assert q("SELECT count(*), count(DISTINCT c.name) FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE p.category = 'sweet'") == [(5, 2)]
assert q("SELECT DISTINCT c.name FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE p.category = 'sweet' ORDER BY 1") == [("Bhavin",), ("Disha",)]
# source: https://datalemur.com
# confirmed: page title "DataLemur - Ace the SQL & Data Science Interview", so it offers SQL interview questions
# source: https://www.stratascratch.com
# confirmed: page title "Data Science & AI Interview Prep | StrataScratch" and it lists SQL, so it offers SQL interview questions
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "for each row in T1 that does not satisfy the join condition with any row in T2, a joined row is added with null values in columns of T2"; only Esha has no order
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL") == [(1,)]
