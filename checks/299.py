# checks for notes/299-hash-join-build-a-hash-table-then-look-up-each-row.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM customers")[0][0] == 5 and q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT order_id, customer_id FROM orders ORDER BY 1") == [(101,1),(102,2),(103,1),(104,3),(105,4),(106,1),(107,2)]
assert 7 * 5 == 35 and 5 + 7 == 12 and 100000 * 5 == 500000 and 5 + 100000 == 100005
assert 2126.11 < 3940.88  # costs from note 298
assert q("SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)") == [("Esha",)]
# source: https://www.postgresql.org/docs/16/planner-optimizer.html
#   confirmed: hash join loads the right relation into a hash table, then scans the left and uses its join values as hash keys
# source: https://www.postgresql.org/docs/16/xoper-optimization.html
#   confirmed: hash join is only for operators that represent equality, since values in different hash buckets are never compared
