# checks for notes/157-on-how-a-join-decides-which-rows-match.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
base = "FROM orders JOIN customers ON orders.customer_id = customers.customer_id"
assert q("SELECT count(*) " + base) == [(7,)]
assert q("SELECT count(*) " + base + " AND customers.city = 'Jersey City'") == [(4,)]
assert q("SELECT count(*) FROM orders JOIN customers ON true") == [(35,)]
assert q("SELECT count(*) FROM orders") == [(7,)] and q("SELECT count(*) FROM customers") == [(5,)]
assert 7 * 5 == 35 and 35 - 7 == 28
# the 4 orders are Asha's 3 and Chirag's 1, both Jersey City
assert q("SELECT name, count(*) " + base + " AND customers.city = 'Jersey City' GROUP BY name ORDER BY name") == [('Asha', 3), ('Chirag', 1)]
# for an inner join, the city test in ON or in WHERE keeps the same rows
assert q("SELECT count(*) " + base + " WHERE customers.city = 'Jersey City'") == [(4,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: a cross join gives "a Cartesian product" with N * M rows, and "FROM T1 CROSS JOIN T2 is equivalent to FROM T1 INNER JOIN T2 ON TRUE"
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model." (the note calls Postgres a server database)
