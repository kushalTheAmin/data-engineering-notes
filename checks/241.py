# checks for notes/241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the real shop has one pending order (106); imagined 108 makes 2
assert q("SELECT order_id FROM orders WHERE status = 'pending'") == [(106,)]
pending = 1 + 1
assert pending == 2
# repeatable read: both cancel a different row, 2 - 1 - 1 = 0 left
assert pending - 1 - 1 == 0
# serializable: esha retried, counts 2 - 1 = 1 and stops
assert pending - 1 == 1
# check yourself 1: real table has 0 pending once 106 is excluded, plus imagined 108 is 1
assert q("SELECT count(*) FROM orders WHERE status = 'pending' AND order_id <> 106")[0][0] == 0
assert 0 + 1 == 1
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): serializable guarantees "the same effect as running them one at a time in some order"; error "could not serialize access due to read/write dependencies among transactions" with SQLSTATE 40001; "applications using this level must be prepared to retry transactions due to serialization failures"; "very hard to predict exactly which transactions might contribute to the read/write dependencies and need to be rolled back"; "doesn't always prevent errors from being raised that would not occur in true serial execution"
# source: https://www.postgresql.org/docs/current/sql-begin.html
#   confirmed (opened this run): BEGIN takes "ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }"
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "In PostgreSQL these locks do not cause any blocking" (so serializable lets both run); Table 13.1 repeatable read: serialization anomaly "Possible"
