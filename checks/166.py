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
# the zones table has 4 rows: 3 named cities and the catch-all
assert q("SELECT count(*) FROM delivery_zones") == [(4,)]
assert q("SELECT count(*) FROM delivery_zones a JOIN delivery_zones b ON a.city = b.city") == [(3,)]
# a second NULL zone row fans Esha out to 2 rows
con.execute("INSERT INTO delivery_zones VALUES (NULL, 'review')")
assert q("SELECT count(*) FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city WHERE c.name = 'Esha'") == [(2,)]

# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed on that page: "NULL IS DISTINCT FROM NULL → f (rather than NULL)", so IS NOT DISTINCT FROM treats two NULLs as equal in Postgres
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed on that page: an inner join gives "a row for each row in T2 that satisfies the join condition", so a pair whose test is unknown (NULL = NULL) is not kept
# source: https://duckdb.org/docs/2.0/sql/expressions/comparison_operators.html
# confirmed on that page: "IS NOT DISTINCT FROM | equal, including NULL | NULL IS NOT DISTINCT FROM NULL | true", so DuckDB has it too
