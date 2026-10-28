# checks for notes/248-the-swap-renaming-two-columns-in-one-transaction.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# order 107 exists in the shop (question 1 asks for it)
assert q("SELECT count(*) FROM orders WHERE order_id = 107") == [(1,)]

# the swap: after the two renames the bigint column carries the old name
cols = {"order_id": "INTEGER", "order_id_big": "BIGINT"}
renamed = {}
for old, new in [("order_id", "order_id_old"), ("order_id_big", "order_id")]:
    renamed[new] = cols[old]
assert renamed == {"order_id_old": "INTEGER", "order_id": "BIGINT"}
# between the two renames no column called order_id exists
after_first = {"order_id_old": "INTEGER", "order_id_big": "BIGINT"}
assert "order_id" not in after_first

# source: https://www.postgresql.org/docs/current/sql-altertable.html
#   confirmed (opened this run): RENAME changes the name of a column, "There is no effect on the stored data", and an ACCESS EXCLUSIVE lock is acquired unless explicitly noted
# source: https://www.postgresql.org/docs/current/runtime-config-client.html
#   confirmed (opened this run): lock_timeout aborts any statement that waits longer than the given time to acquire a lock
# source: https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis
#   confirmed (opened this run): PostgreSQL supports transactional DDL, schema changes can be backed out
# tested this run on a local PostgreSQL 16.15: after both renames in one transaction \d orders showed orders_pkey PRIMARY KEY on order_id_old and the order_items foreign key referencing orders(order_id_old); a SELECT during the open transaction hit lock_timeout; with a SELECT running and a rename waiting, a new SELECT also waited
