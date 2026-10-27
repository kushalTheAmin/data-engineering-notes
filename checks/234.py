# checks for notes/234-replaying-the-log-after-a-crash.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# order 106 is a real shop row and it is pending
assert q("SELECT status FROM orders WHERE order_id = 106") == [("pending",)]
# the replay loop: record 1 skipped (1 <= applied 1), record 2 redone, 108 appears once
applied = 1
done = [n for n in (1, 2) if n > applied]
assert done == [2]
# source: https://www.postgresql.org/docs/current/wal-internals.html
#   confirmed (opened this run): at the start of recovery the server reads the checkpoint record and performs REDO by scanning forward from the WAL location it indicates
# source: https://www.postgresql.org/docs/current/storage-page-layout.html
#   confirmed (opened this run): each page header has pd_lsn, the LSN of the WAL record for the last change to that page
# source: https://raw.githubusercontent.com/postgres/postgres/master/src/backend/access/transam/README
#   confirmed (opened this run): "During WAL replay, we can check the LSN of a page to detect whether the change recorded by the current log entry is already applied (it has been, if the page LSN is >= the log entry's WAL location)"
# toy: redoing the insert (record 1) a second time would give two 108 rows
rows = [108]; rows.append(108); assert rows.count(108) == 2
# page size 8 kB default: https://www.postgresql.org/docs/current/storage-page-layout.html (default 8 kB pages)
# page = 8192 bytes = 2 blocks of 4096 (note 044)
assert 8 * 1024 // 4096 == 2
# source: https://www.postgresql.org/docs/current/wal-intro.html
#   confirmed (opened this run): "in the event of a crash we will be able to recover the database using the log: any changes that have not been applied to the data pages can be redone from the WAL records"
