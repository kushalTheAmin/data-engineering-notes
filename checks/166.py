# checks for notes/166-joining-on-columns-that-can-be-null.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city = z.city ORDER BY c.customer_id") == [('Asha', 'north'), ('Bhavin', 'south'), ('Chirag', 'north'), ('Disha', 'north')]
r = q("SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city ORDER BY c.customer_id")
assert r == [('Asha', 'north'), ('Bhavin', 'south'), ('Chirag', 'north'), ('Disha', 'north'), ('Esha', 'unassigned')] and len(r) == 5
assert q("SELECT NULL = NULL") == [(None,)]
assert None == None  # python: None == None is True
assert q("SELECT c.name, z.zone FROM customers c LEFT JOIN delivery_zones z ON c.city = z.city WHERE c.name = 'Esha'") == [('Esha', None)]
# the catch-all row exists, and customers has exactly one NULL city
assert q("SELECT count(*) FROM delivery_zones WHERE city IS NULL") == [(1,)]
assert q("SELECT count(*) FROM customers WHERE city IS NULL") == [(1,)]
assert q("SELECT count(*) FROM delivery_zones a JOIN delivery_zones b ON a.city = b.city") == [(3,)]
# a second NULL zone row fans Esha out to 2 rows
con.execute("INSERT INTO delivery_zones VALUES (NULL, 'review')")
assert q("SELECT count(*) FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city WHERE c.name = 'Esha'") == [(2,)]

# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed on that page: "NULL IS DISTINCT FROM NULL → f (rather than NULL)", so IS NOT DISTINCT FROM treats two NULLs as equal in Postgres
