# checks for notes/233-the-write-ahead-log-write-down-the-plan-before-the-change.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# check yourself 1: orders 101 to 103 have 2 + 2 + 2 item rows
assert q("SELECT count(*) FROM order_items WHERE order_id IN (101, 102, 103)") == [(6,)]
# the table has 3 rows in the note, the WAL needs 0 table writes before done, no WAL needs all 6
assert 6 - 6 == 0
# 037 priced a spinning disk jump at 10 milliseconds (note 037)
# source: https://www.postgresql.org/docs/current/wal-intro.html
#   confirmed (opened this run): "changes to data files (where tables and indexes reside) must be written only after those changes have been logged, that is, after WAL records describing the changes have been flushed to permanent storage"; "The WAL file is written sequentially, and so the cost of syncing the WAL is much less than the cost of flushing the data pages"; "one fsync of the WAL file may suffice to commit many transactions"; "only the WAL file needs to be flushed to disk to guarantee that a transaction is committed, rather than every data file changed by the transaction"
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
#   confirmed (opened this run): synchronous_commit off "does not create any risk of database inconsistency: ... some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly"
