# checks for notes/161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
base = "SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id"
w = q(base + " WHERE o.status = 'delivered' ORDER BY c.name, o.order_id")
assert w == [('Asha', 101), ('Asha', 103), ('Bhavin', 102), ('Bhavin', 107), ('Disha', 105)]
assert len(w) == 5
# same rows as an inner join with the same filter
inner = q("SELECT c.name, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'delivered' ORDER BY c.name, o.order_id")
assert inner == w
# Esha has no orders, Chirag's only order is cancelled
assert q("SELECT status FROM orders WHERE customer_id = 3") == [('cancelled',)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
# test inside ON keeps 7 rows
on = q(base + " AND o.status = 'delivered' ORDER BY c.name, o.order_id")
assert len(on) == 7 and ('Chirag', None) in on and ('Esha', None) in on
# check yourself
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'cancelled'") == [(5,)]
assert q("SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'cancelled' WHERE o.order_id IS NOT NULL") == [('Chirag',)]
assert q("SELECT order_id FROM orders WHERE status = 'cancelled'") == [(104,)]
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'") == [(4,)]
assert q("SELECT count(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'") == [(4,)]
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND c.city = 'Jersey City'") == [(7,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "a restriction placed in the ON clause is processed before the join, while a restriction placed in the WHERE clause is processed after the join. That does not matter with inner joins, but it matters a lot with outer joins."
