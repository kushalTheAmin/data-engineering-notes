# checks for notes/250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, 106 pending, 107 delivered; 108 and 109 are imagined
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT status FROM orders WHERE order_id = 106") == [("pending",)]
assert q("SELECT status FROM orders WHERE order_id = 107") == [("delivered",)]
assert q("SELECT count(*) FROM orders WHERE order_id IN (108, 109)")[0][0] == 0

def done(x, snap):
    return x < snap["xmin"] or (x < snap["xmax"] and x not in snap["running"])

def visible(v, snap):
    slot, order, status, xmin, xmax = v
    return done(xmin, snap) and not (xmax != 0 and done(xmax, snap))

versions = [(6, 106, "pending", 738, 739), (7, 107, "delivered", 738, 0), (8, 106, "delivered", 739, 0), (9, 108, "pending", 740, 0)]
first = {"xmin": 739, "xmax": 741, "running": [739]}
later = {"xmin": 741, "xmax": 741, "running": []}
assert [visible(v, first) for v in versions] == [True, True, False, True]
assert [visible(v, later) for v in versions] == [False, True, True, True]
# 740 is bigger than 739 yet visible, 739 is smaller yet not
assert done(740, first) and not done(739, first)
# check yourself 1: 741 is not below xmax 741, so it hadnt finished at the first snapshot
assert not done(741, first)
# a new query at read committed takes a new snapshot where 741 is finished
assert done(741, {"xmin": 742, "xmax": 742, "running": []})

# source: https://www.postgresql.org/docs/16/functions-info.html
#   confirmed (opened this run): pg_current_snapshot prints xmin:xmax:xip_list, ids below xmin are finished, ids at or above xmax are not, ids in between are finished unless in xip_list, and finished does not mean committed (it may have rolled back)
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed (opened this run): "the row version must not be deleted while it is still potentially visible to other transactions"
# tested this run on a local PostgreSQL 16.15: setup insert was xid 738, Asha 739 (open update of 106), Bhavin 740 (insert 108, committed); a repeatable read session then printed pg_current_snapshot as 739:741:739, read versions at slots 6, 7, 9 and not slot 8; after Asha committed, a new transaction printed 741:741: and read slots 7, 8, 9; the first session kept reading slot 6
#   also tested: a repeatable read session took its first query, another session committed an insert, the repeatable read count stayed 8 while a read committed session went from 8 to 9; a rolled back insert was never visible; VACUUM VERBOSE with the repeatable read transaction open reported "1 are dead but not yet removable", and after it ended "0 are dead but not yet removable" with the dead version removed
# source: https://www.postgresql.org/docs/16/transaction-iso.html
#   confirmed (opened this run): "SELECT does see the effects of previous updates executed within its own transaction, even though they are not yet committed" (read committed); repeatable read queries also "see the effects of previous updates executed within its own transaction"
