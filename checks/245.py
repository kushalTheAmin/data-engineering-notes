# checks for notes/245-changing-a-column-type-the-table-rewrite-and-the-lock.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# orders 101, 102, 103 exist in the shop
assert q("SELECT order_id FROM orders WHERE order_id IN (101, 102, 103) ORDER BY order_id") == [(101,), (102,), (103,)]
# a 32 bit integer tops out at 2147483647
assert 2 ** 31 - 1 == 2147483647
# 4 bytes before, 8 bytes after
for i in (101, 102, 103):
    assert list(i.to_bytes(4, "big")) == [0, 0, 0, i]
    assert list(i.to_bytes(8, "big")) == [0, 0, 0, 0, 0, 0, 0, i]
# 50 GB table, up to double is 100 GB, so another 50 GB free
assert 50 * 2 == 100 and 100 - 50 == 50  # a ceiling
# source: https://www.postgresql.org/docs/current/sql-altertable.html
#   confirmed (opened this run): ACCESS EXCLUSIVE lock is acquired unless explicitly noted; changing the type of an existing column will normally cause the entire table and its indexes to be rewritten; exception when USING does not change contents and old type is binary coercible to new; rebuilds may take a long time and temporarily require as much as double the disk space
# source: https://www.postgresql.org/docs/current/datatype-numeric.html
#   confirmed (opened this run): integer is 4 bytes, range -2147483648 to +2147483647, bigint is 8 bytes
# source: https://www.postgresql.org/docs/current/explicit-locking.html
#   confirmed (opened this run): ACCESS EXCLUSIVE conflicts with locks of all modes including ACCESS SHARE, which SELECT takes; many forms of ALTER TABLE acquire a lock at this level; an ACCESS EXCLUSIVE lock blocks a plain SELECT
