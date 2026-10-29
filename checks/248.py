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
# the trigger from 247 names order_id_big, so after the renames it points at a column that is gone; flipped, it names order_id_old
trigger_target = "order_id_big"
assert trigger_target not in renamed and "order_id_old" in renamed
# tested this run on a local PostgreSQL 16.15: with the 247 trigger left alone, after the swap every INSERT and UPDATE on orders failed with
#   record "new" has no field "order_id_big"; with the trigger dropped instead, an INSERT that sets only order_id failed with
#   null value in column "order_id_old" violates not-null constraint (the primary key stayed on order_id_old);
#   with CREATE OR REPLACE FUNCTION copy_order_id() setting NEW.order_id_old := NEW.order_id inside the same transaction, INSERT of 108 and an UPDATE both worked
# source: https://www.postgresql.org/docs/16/datatype-numeric.html
#   confirmed (opened this run): Table 8.2 lists integer as 4 bytes and bigint as 8 bytes
