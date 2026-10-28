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
# source: https://www.postgresql.org/docs/current/sql-begin.html
#   confirmed (opened this run): "BEGIN [ WORK | TRANSACTION ] [ transaction_mode [, ...] ]" with "ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }"
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): Table 13.1 repeatable read row: phantom read "Allowed, but not in PG"; "This is a stronger guarantee than is required by the SQL standard for this isolation level"
# source: https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql
#   confirmed (opened this run): SQL Server REPEATABLE READ: "Other transactions can insert new rows that match the search conditions of statements issued by the current transaction ... which results in phantom reads"
# count(*) counts rows, WHERE keeps only matching rows (glossed in check yourself 1)
assert q("SELECT count(*) FROM orders WHERE status = 'pending'")[0][0] == len(q("SELECT * FROM orders WHERE status = 'pending'"))
