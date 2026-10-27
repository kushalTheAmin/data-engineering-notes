# checks for notes/240-repeatable-read-rows-dont-change-under-you-mid-transaction.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, an imagined committed 108 makes 8
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert 7 + 1 == 8
# check yourself 1: one pending order (106) now, still 1 in ashas picture
assert q("SELECT count(*) FROM orders WHERE status = 'pending'")[0][0] == 1
assert q("SELECT status FROM orders WHERE order_id = 106") == [("pending",)]
# check yourself 2: 106 plus imagined pending 108
assert q("SELECT count(*) FROM orders WHERE status = 'pending'")[0][0] + 1 == 2
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): repeatable read "only sees data committed before the transaction began"; "a snapshot as of the start of the first non-transaction-control statement in the transaction"; stronger than the SQL standard requires and prevents phantoms; "could not serialize access due to concurrent update"; "must be prepared to retry transactions due to serialization failures"
