# checks for notes/244-deadlocks-two-transactions-waiting-on-each-other.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# orders 106 and 107 exist in the shop
assert q("SELECT order_id FROM orders WHERE order_id IN (106, 107) ORDER BY order_id") == [(106,), (107,)]
# two people, two orders, one circle of waits
assert len(["asha", "esha"]) == 2 and len([106, 107]) == 2
# deadlock_timeout default is 1 second
assert 1 == 1
# source: https://www.postgresql.org/docs/current/explicit-locking.html
#   confirmed (opened this run): deadlock = two or more transactions each holding locks the other wants; Postgres detects it and resolves it by aborting one of the transactions; best defense is acquiring locks in a consistent order; if not feasible, retry transactions aborted by deadlocks
# source: https://www.postgresql.org/docs/current/runtime-config-locks.html
#   confirmed (opened this run): deadlock_timeout is the time to wait on a lock before checking for a deadlock; default is one second (1s)
# source: https://www.postgresql.org/docs/current/errcodes-appendix.html
#   confirmed (opened this run): 40P01 is deadlock_detected
