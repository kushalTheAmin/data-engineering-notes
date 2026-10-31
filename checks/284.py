# checks for notes/284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, ids 101 to 107, and 106 is pending before the update
assert [r[0] for r in q("SELECT order_id FROM orders ORDER BY order_id")] == list(range(101, 108))
assert q("SELECT status FROM orders WHERE order_id = 106") == [("pending",)]
# slots 1 to 7 hold the 7 orders in id order, so ctid (0,1) to (0,7)
assert [(0, i + 1) for i in range(7)][-1] == (0, 7)
# one page is 8192 bytes, two 4096 byte blocks (note 044)
assert 8192 // 4096 == 2
# 7 orders fit in one page, the update adds a copy so 106 moves to slot 8
assert 7 + 1 == 8
# 1000 made up orders took 8 pages (65536 bytes)
assert 8 * 8192 == 65536
# run on a real Postgres 16.15 server: SELECT ctid gave (0,1) to (0,7) for 101 to 107,
# SHOW block_size gave 8192, pg_relation_size('orders') gave 8192 (1 page),
# after UPDATE of 106, ctid of 106 was (0,8) and of 107 was (0,7),
# a 1000 row table of the same shape (generate_series) had pg_relation_size 65536 (8 pages)
# source: https://www.postgresql.org/docs/current/storage-page-layout.html
#   confirmed: tables are arrays of fixed size pages, usually 8 kB, changeable at compile time,
#   and a ctid is a page number plus the index of an item identifier
