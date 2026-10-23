# checks for notes/174-subquery-in-where.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
inner = "SELECT customer_id FROM orders WHERE status = 'delivered'"
# the inner list: one id per delivered order, in order id order
assert q(inner.replace("FROM orders", "FROM orders") + " ORDER BY order_id") == [(1,), (2,), (1,), (4,), (2,)]
assert q("SELECT name FROM customers WHERE customer_id IN (" + inner + ") ORDER BY name") == [("Asha",), ("Bhavin",), ("Disha",)]
# the join version repeats Asha and Bhavin: 5 rows
assert q("SELECT c.name FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'delivered' ORDER BY c.name") == [("Asha",), ("Asha",), ("Bhavin",), ("Bhavin",), ("Disha",)]
# the trace table: chirag 3 and esha 5 are not in the list
ids = [r[0] for r in q(inner)]
assert [(n, i in ids) for i, n in q("SELECT customer_id, name FROM customers ORDER BY customer_id")] == [("Asha", True), ("Bhavin", True), ("Chirag", False), ("Disha", True), ("Esha", False)]
# check yourself 1: order ids 101 to 107 never equal a customer id 1 to 5
assert q("SELECT name FROM customers WHERE customer_id IN (SELECT order_id FROM orders WHERE status = 'delivered')") == []
assert q("SELECT min(order_id), max(order_id) FROM orders") == [(101, 107)] and q("SELECT min(customer_id), max(customer_id) FROM customers") == [(1, 5)]
# check yourself 2: 7 ids in the list, 4 customers match, esha has no order
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM customers WHERE customer_id IN (SELECT customer_id FROM orders)") == [(4,)]
# check yourself 3: chirag cancelled 104, asha pending 106
assert q("SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders WHERE status <> 'delivered') ORDER BY name") == [("Asha",), ("Chirag",)]
assert q("SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'pending'") == [(106,)]
# source: https://www.postgresql.org/docs/current/functions-subquery.html
# confirmed: "The right-hand side is a parenthesized subquery, which must return exactly one column." and "The result of IN is "true" if any equal subquery row is found."
