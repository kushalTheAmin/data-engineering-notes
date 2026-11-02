# checks for notes/300-merge-join-walk-two-sorted-lists-side-by-side.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM customers")[0][0] == 5 and q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT order_id, customer_id FROM orders ORDER BY customer_id, order_id") == [(101,1),(103,1),(106,1),(102,2),(107,2),(104,3),(105,4)]
assert [c for o, c in q("SELECT order_id, customer_id FROM orders ORDER BY order_id")] == [1, 2, 1, 3, 4, 1, 2]
# the walk: 7 order steps plus 3 customer moves
assert 7 + 3 == 10
assert q("SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)") == [("Esha",)]
# source: https://www.postgresql.org/docs/16/planner-optimizer.html
#   confirmed: merge join sorts each relation on the join attributes, scans both in parallel, sorting can come from an explicit sort or an index scan in the proper order
# source: https://www.postgresql.org/docs/16/xoper-optimization.html
#   confirmed: a merge-joinable operator must behave like equality
# audit: the note said markers only move forward and cited the docs, but the docs only say each relation has to be scanned only once. Postgres source nodeMergejoin.c marks the first inner tuple of a run of equal keys and restores the inner cursor to it for the next outer row with the same key
# source: https://raw.githubusercontent.com/postgres/postgres/REL_16_STABLE/src/backend/executor/nodeMergejoin.c
#   confirmed: comment says the inner cursor is repositioned by marking the first inner 5 so the executor can restore the cursor to it, and the access method provides routines to mark and restore to a tuple (opened this run)
