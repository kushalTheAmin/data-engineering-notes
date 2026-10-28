# checks for notes/242-row-locks-and-table-locks.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# 106 is pending and 107 is delivered in the real shop
assert q("SELECT order_id, status FROM orders WHERE order_id IN (106, 107) ORDER BY order_id") == [(106, 'pending'), (107, 'delivered')]
# source: https://www.postgresql.org/docs/current/explicit-locking.html
#   confirmed (opened this run): "Row-level locks do not affect data querying; they block only writers and lockers to the same row"; "Row-level locks are released at transaction end"; ACCESS EXCLUSIVE is acquired by DROP TABLE and TRUNCATE (and many forms of ALTER TABLE); "Only an ACCESS EXCLUSIVE lock blocks a SELECT (without FOR UPDATE/SHARE) statement"
#   confirmed (opened this run): "Once acquired, a lock is normally held until the end of the transaction. But if a lock is acquired after establishing a savepoint, the lock is released immediately if the savepoint is rolled back to" (so the note says normally held)
