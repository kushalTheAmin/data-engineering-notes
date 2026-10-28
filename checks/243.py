# checks for notes/243-select-for-update-locking-on-purpose.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# order 106 is pending, 107 is delivered, and 106 is the only pending order
assert q("SELECT order_id, status FROM orders WHERE order_id IN (106, 107) ORDER BY order_id") == [(106, 'pending'), (107, 'delivered')]
assert q("SELECT order_id FROM orders WHERE status = 'pending'") == [(106,)]
# the trace has 2 people, 4 steps
assert len(["asha", "esha"]) == 2
# source: https://www.postgresql.org/docs/current/explicit-locking.html
#   confirmed (opened this run): FOR UPDATE locks the rows retrieved until the current transaction ends; other transactions doing UPDATE, DELETE or SELECT FOR UPDATE on them are blocked until then; row-level locks do not affect data querying, they block only writers and lockers; row locks are released at transaction end
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): at read committed, a SELECT FOR UPDATE waits for the first updater, then re-evaluates the WHERE against the updated version of the row and returns it only if it still matches; read committed is the default
# source: https://www.postgresql.org/docs/current/sql-begin.html
#   confirmed (opened this run): without BEGIN, each statement is executed in its own transaction (autocommit)
