# checks for notes/178-exists-and-not-exists-asking-whether-a-matching-row-exists.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
orders = [(101, 1, "delivered"), (102, 2, "delivered"), (103, 1, "delivered"), (104, 3, "cancelled"), (105, 4, "delivered"), (106, 1, "pending"), (107, 2, "delivered")]
customers = [(1, "Asha"), (2, "Bhavin"), (3, "Chirag"), (4, "Disha"), (5, "Esha")]
assert q("SELECT order_id, customer_id, status FROM orders ORDER BY order_id") == orders
assert q("SELECT customer_id, name FROM customers ORDER BY customer_id") == customers
res = {n: len([o for o in orders if o[1] == c and o[2] == "delivered"]) for c, n in customers}
assert res == {"Asha": 2, "Bhavin": 2, "Chirag": 0, "Disha": 1, "Esha": 0}
E_ = "EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered')"
assert q(f"SELECT name FROM customers c WHERE {E_} ORDER BY name") == [("Asha",), ("Bhavin",), ("Disha",)]
assert q(f"SELECT name FROM customers c WHERE NOT {E_} ORDER BY name") == [("Chirag",), ("Esha",)]
# a join repeats Asha and Bhavin: 5 rows
assert len(q("SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'delivered'")) == 5
# the select list never matters
for sel in ("1", "*", "NULL"):
    assert q(f"SELECT name FROM customers c WHERE EXISTS (SELECT {sel} FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered') ORDER BY name") == [("Asha",), ("Bhavin",), ("Disha",)]
# check yourself 1: no correlation keeps all 5
assert q("SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.status = 'delivered') ORDER BY name") == [("Asha",), ("Bhavin",), ("Chirag",), ("Disha",), ("Esha",)]
# check yourself 2: Asha has a pending order, Chirag a cancelled one
assert q("SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status <> 'delivered') ORDER BY name") == [("Asha",), ("Chirag",)]
# source: https://www.postgresql.org/docs/current/functions-subquery.html
# confirmed: EXISTS is true if the subquery returns at least one row, false if none; the subquery is generally run only long enough to find whether a row exists; the output list is normally unimportant
# source: https://en.wikipedia.org/wiki/Semijoin
# confirmed: "The result is the set of all tuples in R for which there is a tuple in S that is equal on their common attribute names. The difference from a natural join is that other columns of S do not appear."
# the select list is only "normally unimportant", the docs name exceptions such as subqueries that use INTERSECT
# confirmed: "the output list of the subquery is normally unimportant. A common coding convention is to write all EXISTS tests in the form EXISTS(SELECT 1 WHERE ...) . There are exceptions to this rule however, such as subqueries that use INTERSECT ."
# check yourself 2: NOT EXISTS with the original test keeps Chirag and Esha, so the tempting Chirag only comes from ruling Asha out, not from that reading
assert q("SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered') ORDER BY name") == [("Chirag",), ("Esha",)]
