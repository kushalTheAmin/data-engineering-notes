# checks for notes/115-is-null-and-is-not-null.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda w: [r[0] for r in con.execute("SELECT name FROM customers WHERE " + w).fetchall()]
assert len(con.execute("SELECT 1 FROM customers").fetchall()) == 5
assert q("city = NULL") == []
assert q("city IS NULL") == ["Esha"]
assert q("city IS NOT NULL") == ["Asha", "Bhavin", "Chirag", "Disha"]
assert len(q("city IS NULL")) + len(q("city IS NOT NULL")) == 5 == 1 + 4
r = con.execute("SELECT name, city = NULL, city IS NULL, city IS NOT NULL FROM customers ORDER BY customer_id").fetchall()
assert all(x[1] is None for x in r)
assert [x[2] for x in r] == [False, False, False, False, True]
assert [x[3] for x in r] == [True, True, True, True, False]
assert len(r) == 5
assert (None == None) is True
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: IS NULL / IS NOT NULL test for a null; "Do not write expression = NULL because NULL is not 'equal to' NULL"
print("115 ok")
