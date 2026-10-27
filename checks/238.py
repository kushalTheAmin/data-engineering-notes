# checks for notes/238-phantoms.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders and exactly one pending, order 106
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT order_id FROM orders WHERE status = 'pending'") == [(106,)]
assert q("SELECT order_id FROM orders WHERE order_id IN (105, 106, 107) ORDER BY order_id") == [(105,), (106,), (107,)]
# check yourself 1: one pending now, a committed pending 108 makes it two
assert q("SELECT count(*) FROM orders WHERE status = 'pending'")[0][0] == 1
assert q("SELECT count(*) FROM orders WHERE status = 'pending'")[0][0] + 1 == 2
# check yourself 2: three snacks, a new snack makes four
assert q("SELECT count(*) FROM products WHERE category = 'snack'")[0][0] == 3
assert 3 + 1 == 4
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "phantom read: A transaction re-executes a query returning a set of rows that satisfy a search condition and finds that the set of rows satisfying the condition has changed due to another recently-committed transaction"; Table 13.1 lists phantom read Possible at Read committed and "Allowed, but not in PG" at Repeatable read; "Read Committed is the default isolation level"
