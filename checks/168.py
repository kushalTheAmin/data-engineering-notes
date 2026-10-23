# checks for notes/168-self-join-a-table-joined-to-itself.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the python loop in the note: same data as customers, NULL city never matches
rows = q("SELECT name, city FROM customers ORDER BY customer_id")
assert rows == [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
pairs = [(a[0], b[0]) for a in rows for b in rows if a[1] is not None and a[1] == b[1]]
assert pairs == [("Asha", "Asha"), ("Asha", "Chirag"), ("Bhavin", "Bhavin"), ("Chirag", "Asha"), ("Chirag", "Chirag"), ("Disha", "Disha")]
# 6 lines, 4 of them a customer with herself, 1 mirrored pair
assert len(pairs) == 6
assert sum(1 for a, b in pairs if a == b) == 4
assert q("SELECT count(*) FROM customers a JOIN customers b ON a.city = b.city") == [(6,)]
assert q("SELECT a.name, b.name AS lives_near FROM customers a JOIN customers b ON a.city = b.city AND a.customer_id < b.customer_id") == [("Asha", "Chirag")]
# Esha has a NULL city so she is in no pair
assert q("SELECT city FROM customers WHERE name = 'Esha'") == [(None,)]
assert q("SELECT customer_id FROM customers WHERE name IN ('Asha','Chirag') ORDER BY name") == [(1,), (3,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: aliases are necessary when joining a table to itself, with the example people AS mother JOIN people AS child ON mother.id = child.mother_id
# source: https://www.postgresql.org/docs/current/tutorial-join.html
# confirmed: the tutorial calls joining a table against itself a self join
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "The ON clause is the most general kind of join condition: it takes a Boolean value expression of the same kind as is used in a WHERE clause."
