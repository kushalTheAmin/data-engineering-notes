# checks for notes/266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md
import os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
q = lambda con, s: con.execute(s).fetchall()
CUT = "SELECT count(*) FROM customer_accounts WHERE updated_at > TIMESTAMP '2026-04-10 00:00:00'"
# the shop table is the soft deleted state: 4 rows, Disha soft deleted
con = shop()
assert q(con, "SELECT count(*) FROM customer_accounts") == [(4,)]
assert q(con, "SELECT customer_id FROM customer_accounts WHERE deleted_at IS NOT NULL") == [(4,)]
assert q(con, "SELECT 'no filter' AS query, count(*) AS accounts FROM customer_accounts UNION ALL SELECT 'live only', count(*) FROM customer_accounts WHERE deleted_at IS NULL") == [("no filter", 4), ("live only", 3)]
# soft delete column: the copy job finds Disha, and her deleted_at says 09:00
assert q(con, CUT) == [(1,)]
assert q(con, "SELECT deleted_at FROM customer_accounts WHERE customer_id = 4") == [(datetime(2026, 4, 10, 9, 0),)]
# table: soft delete leaves 4 rows. hard delete leaves 3 and the copy job finds nothing
hard = shop()
hard.execute("DELETE FROM customer_accounts WHERE customer_id = 4")
assert q(hard, "SELECT count(*) FROM customer_accounts") == [(3,)]
assert q(hard, CUT) == [(0,)]
# running the note's UPDATE on a fresh live row gives the same soft state
soft = shop()
soft.execute("UPDATE customer_accounts SET deleted_at = NULL, updated_at = TIMESTAMP '2026-03-02 10:00:00' WHERE customer_id = 4")
soft.execute("UPDATE customer_accounts SET deleted_at = TIMESTAMP '2026-04-10 09:00:00', updated_at = TIMESTAMP '2026-04-10 09:00:00' WHERE customer_id = 4")
assert q(soft, "SELECT count(*) FROM customer_accounts") == [(4,)]
assert q(soft, CUT) == [(1,)]
# question 1: live rows have NULL deleted_at so <> is unknown, Disha equals the time
assert q(con, "SELECT count(*) AS n FROM customer_accounts WHERE deleted_at <> TIMESTAMP '2026-04-10 09:00:00'") == [(0,)]
assert q(con, "SELECT count(*) FROM customer_accounts WHERE deleted_at IS NULL") == [(3,)]
# question 2: UNIQUE email refuses a second disha@example.com while the soft deleted row stays
try:
    con.execute("INSERT INTO customer_accounts VALUES (5, 'disha@example.com', TIMESTAMP '2026-05-10 09:00:00', NULL)")
    raise SystemExit("should have failed")
except Exception as e:
    assert "Constraint" in type(e).__name__ or "onstraint" in str(e)
hard.execute("INSERT INTO customer_accounts VALUES (5, 'disha@example.com', TIMESTAMP '2026-05-10 09:00:00', NULL)")
assert q(hard, "SELECT count(*) FROM customer_accounts") == [(4,)]
# hard delete is blocked by foreign keys: Disha has order 105, so her customers row cannot be deleted
assert q(con, "SELECT count(*) FROM orders WHERE customer_id = 4") == [(1,)]
