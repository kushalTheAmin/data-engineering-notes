# checks for notes/251-backups-a-copy-you-can-restore-from.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 real orders, 101 to 107; 108 is imagined
assert [r[0] for r in q("SELECT order_id FROM orders ORDER BY order_id")] == [101, 102, 103, 104, 105, 106, 107]
assert q("SELECT count(*) FROM orders WHERE order_id = 108")[0][0] == 0

live = [101, 102, 103, 104, 105, 106, 107]
backup = list(live)
assert len(backup) == 7
live.append(108)
assert len(live) == 8 and len(backup) == 7
# a second name for the same list changes both
alias = backup
alias.append(999)
assert 999 in backup
backup.remove(999)
live = list(backup)
assert len(live) == 7 and 108 not in live
# source: https://www.postgresql.org/docs/current/app-pgdump.html
# confirmed: pg_dump makes consistent exports even if the database is used concurrently, does not block readers or writers, and except in simple cases is generally not the right choice for regular production backups
# source: https://www.postgresql.org/docs/current/app-pgdump.html
# confirmed: the default pg_dump output format is a plain-text SQL script file
# source: https://www.postgresql.org/docs/16/wal-intro.html
# confirmed (opened this run): "any changes that have not been applied to the data pages can be redone from the WAL records. (This is roll-forward recovery, also known as REDO.)"
print("251 ok")
