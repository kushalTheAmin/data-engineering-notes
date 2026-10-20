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
# IS NULL and IS NOT NULL give true or false, never unknown, for a null and for a value
assert con.execute("SELECT NULL IS NULL, 1 IS NULL, NULL IS NOT NULL, 1 IS NOT NULL").fetchone() == (True, False, False, True)
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: "datatype IS NULL → boolean  Test whether value is null" and IS NOT NULL likewise, so they return a plain boolean; IS NULL / IS NOT NULL test for a null; "Do not write expression = NULL because NULL is not 'equal to' NULL"
assert q("city IS NOT DISTINCT FROM NULL") == ["Esha"]
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: IS [NOT] DISTINCT FROM "effectively act as though null were a normal data value, rather than unknown"; NULL IS NOT DISTINCT FROM NULL is t
print("115 ok")
