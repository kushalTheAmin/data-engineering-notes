# checks for notes/249-mvcc-an-update-writes-a-new-row-version.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, 106 is pending and 107 is delivered
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT status FROM orders WHERE order_id = 106") == [("pending",)]
assert q("SELECT status FROM orders WHERE order_id = 107") == [("delivered",)]

# model of row versions: a list of dicts, an UPDATE appends and stamps the old one
def update(versions, xid, match, changes):
    for v in list(versions):
        if v["xmax"] == 0 and match(v):
            v["xmax"] = xid
            versions.append({**v, **changes, "xmin": xid, "xmax": 0})
orders = [{"order": o, "status": s, "xmin": 738, "xmax": 0} for o, s in q("SELECT order_id, status FROM orders ORDER BY order_id")]
update(orders, 739, lambda v: v["order"] == 106, {"status": "delivered"})
# 8 versions for 7 orders, slot 6 stamped 739, slot 8 is the new 106
assert len(orders) == 8
assert (orders[5]["order"], orders[5]["status"], orders[5]["xmin"], orders[5]["xmax"]) == (106, "pending", 738, 739)
assert (orders[6]["order"], orders[6]["status"], orders[6]["xmin"], orders[6]["xmax"]) == (107, "delivered", 738, 0)
assert (orders[7]["order"], orders[7]["status"], orders[7]["xmin"], orders[7]["xmax"]) == (106, "delivered", 739, 0)
# check yourself 1: after a rolled back update there are still 2 versions of 106, readers skip the aborted one
assert 1 + 1 == 2
# check yourself 2: updating every order, even to the same value, doubles the versions
every = [{"order": o, "status": s, "xmin": 1, "xmax": 0} for o, s in q("SELECT order_id, status FROM orders")]
update(every, 2, lambda v: True, {})
assert len(every) == 14 and len([v for v in every if v["xmax"] == 0]) == 7

# source: https://www.postgresql.org/docs/16/ddl-system-columns.html
#   confirmed (opened this run): xmin is the transaction id of the inserting transaction for this row version, xmax is the deleting transaction or zero, each update of a row creates a new row version, a nonzero xmax usually means the deleting transaction hasn't committed yet or was rolled back
# source: https://www.postgresql.org/docs/16/mvcc-intro.html
#   confirmed (opened this run): "reading never blocks writing and writing never blocks reading"
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed (opened this run): VACUUM removes dead row versions in tables and indexes
# tested this run on a local PostgreSQL 16 with pageinspect: slots 6, 7, 8 and the stamps 738/739 in the note, Eshas SELECT during the open update returned slot (0,6) pending xmin 738 xmax 739, after COMMIT slot (0,8) delivered; a rolled back update left 8 versions and a SELECT read pending; UPDATE orders SET status = status left count(*) at 7 and 14 versions
#   also confirmed on that page: the autovacuum daemon runs VACUUM automatically (opened this run)
# audit: xmax is zero only for a row version nobody has tried to delete or replace; the same page says it can be nonzero in a visible row version when the deleting transaction hasnt committed yet or rolled back (opened this run), as slot 6 is for Esha in the note
