# checks for notes/179-not-in-and-the-null-trap.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT name FROM customers WHERE city NOT IN (SELECT city FROM delivery_zones WHERE zone = 'north') ORDER BY name") == [("Bhavin",)]
assert q("SELECT name FROM customers WHERE city NOT IN (SELECT city FROM delivery_zones WHERE zone <> 'south') ORDER BY name") == []
# the list is Jersey City, Hoboken, NULL
assert sorted(q("SELECT city FROM delivery_zones WHERE zone <> 'south'"), key=lambda r: str(r[0])) == [("Hoboken",), ("Jersey City",), (None,)]
# trace: Edison against the list
assert q("SELECT 'Edison' <> 'Jersey City', 'Edison' <> 'Hoboken', 'Edison' <> NULL") == [(True, True, None)]
assert q("SELECT true AND true AND NULL") == [(None,)]
# anyone in the list gets false, only Bhavin and Esha get unknown
res = q("SELECT name, city <> 'Jersey City' AND city <> 'Hoboken' AND city <> NULL FROM customers ORDER BY customer_id")
assert res == [("Asha", False), ("Bhavin", None), ("Chirag", False), ("Disha", False), ("Esha", None)]
assert q("SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM delivery_zones z WHERE z.city = c.city AND z.zone <> 'south') ORDER BY name") == [("Bhavin",), ("Esha",)]
# filtering the NULL out of the list still drops Esha
assert q("SELECT name FROM customers WHERE city NOT IN (SELECT city FROM delivery_zones WHERE zone <> 'south' AND city IS NOT NULL) ORDER BY name") == [("Bhavin",)]
# check yourself
assert q("SELECT name FROM customers WHERE city NOT IN (SELECT city FROM customers WHERE name = 'Esha') ORDER BY name") == []
assert q("SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM customers e WHERE e.name = 'Esha' AND e.city = c.city) ORDER BY name") == [("Asha",), ("Bhavin",), ("Chirag",), ("Disha",), ("Esha",)]
# source: https://www.postgresql.org/docs/current/functions-subquery.html
# confirmed: NOT IN is true if only unequal subquery rows are found; if the left side is null, or no equal values and at least one null row, the result is null, not true
