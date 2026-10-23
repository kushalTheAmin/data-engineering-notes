# checks for notes/183-intersect-and-except.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
D = "SELECT customer_id FROM orders WHERE status = 'delivered'"
N = "SELECT customer_id FROM orders WHERE status <> 'delivered'"
assert q(D) == [(1,), (2,), (1,), (4,), (2,)] or sorted(q(D)) == [(1,), (1,), (2,), (2,), (4,)]
assert sorted(q(N)) == [(1,), (3,)]
assert q(f"{D} INTERSECT {N}") == [(1,)]
assert q(f"{D} EXCEPT {N} ORDER BY customer_id") == [(2,), (4,)]
assert q(f"{N} EXCEPT {D} ORDER BY customer_id") == [(3,)]
assert q("SELECT name FROM customers WHERE customer_id = 3") == [("Chirag",)]
assert q("SELECT status FROM orders WHERE customer_id = 3") == [("cancelled",)]
assert q("SELECT name FROM customers WHERE customer_id = 2") == [("Bhavin",)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 2 AND status = 'delivered'") == [(2,)]
a, b = {1, 2, 4}, {3, 1}
assert a & b == {1} and a - b == {2, 4} and b - a == {3}
# check yourself 1
assert q("SELECT name FROM products WHERE category = 'snack' EXCEPT SELECT name FROM products WHERE price < 6 ORDER BY name") == [("dhokla",), ("khandvi",)]
assert q("SELECT name FROM products WHERE price < 6 EXCEPT SELECT name FROM products WHERE category = 'snack' ORDER BY name") == [("jalebi",), ("masala chai",)]
# check yourself 2
assert q("SELECT city FROM customers WHERE customer_id = 5") == [(None,)]
assert q("SELECT city FROM customers EXCEPT SELECT city FROM customers WHERE customer_id = 5 ORDER BY city") == [("Edison",), ("Hoboken",), ("Jersey City",)]
assert len(q("SELECT city FROM customers EXCEPT SELECT city FROM customers WHERE customer_id = 5")) == 3
# source: https://www.postgresql.org/docs/current/queries-union.html
# confirmed: INTERSECT returns rows in both results, EXCEPT returns rows in the first but not the second, duplicates eliminated unless ALL is used
# plain INTERSECT and EXCEPT drop repeats, the ALL forms keep them
assert q(f"{D} INTERSECT ALL {N}") == [(1,)]
assert q(f"{D} EXCEPT ALL {N} ORDER BY customer_id") == [(1,), (2,), (2,), (4,)]
# source: https://www.postgresql.org/docs/current/queries-union.html
# confirmed: "Duplicate rows are eliminated unless INTERSECT ALL is used." and "Again, duplicates are eliminated unless EXCEPT ALL is used."
# source: https://en.wikipedia.org/wiki/Set_operations_(SQL)
# confirmed: "For purposes of duplicate removal the INTERSECT operator does not distinguish between NULLs." and "For purposes of row elimination and duplicate removal, the EXCEPT operator does not distinguish between NULLs."
assert q("SELECT city FROM customers INTERSECT SELECT city FROM customers WHERE customer_id = 5") == [(None,)]
