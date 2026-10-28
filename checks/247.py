# checks for notes/247-keeping-the-new-column-in-sync-with-a-trigger.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has orders 101 to 107, no 108
assert q("SELECT order_id FROM orders ORDER BY order_id") == [(i,) for i in range(101, 108)]

def run(steps):
    rows = {}
    trigger = False
    for s in steps:
        if s == "trigger":
            trigger = True
        elif s == "backfill":
            for i in range(101, 108):
                rows[i] = i
        elif isinstance(s, int):
            rows[s] = s if trigger else None
    return sum(v is None for v in rows.values())

# trigger first, then 108 placed, then backfill: 0 NULLs
assert run(["trigger", 108, "backfill"]) == 0
# backfill first, then 108 placed, then trigger: 1 NULL
assert run(["backfill", 108, "trigger"]) == 1
# question 1: backfill, then 108 and 109, then trigger: 2 NULLs
assert run(["backfill", 108, 109, "trigger"]) == 2
# source: https://www.postgresql.org/docs/current/plpgsql-trigger.html
#   confirmed (opened this run): NEW is the new row in row-level INSERT/UPDATE triggers, a BEFORE trigger changes the stored row by changing NEW and returning it, and the CREATE FUNCTION ... RETURNS trigger / CREATE TRIGGER ... BEFORE INSERT OR UPDATE ... FOR EACH ROW EXECUTE FUNCTION syntax

