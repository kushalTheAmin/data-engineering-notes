# checks for notes/285-full-table-scan-reading-every-page.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the made up table: order ids 101 to 1100 (1000 rows), 8 pages (note 284)
ids = list(range(101, 1101))
assert len(ids) == 1000
# order 106 is the 6th row, so it sits on the first page
assert ids.index(106) + 1 == 6
# a scan with no LIMIT checks every row: 1 comes out, 999 thrown away
assert len([i for i in ids if i == 106]) == 1 and len([i for i in ids if i != 106]) == 999
# a miss throws away all 1000
assert len([i for i in ids if i != 999999]) == 1000
# LIMIT 1 stops after the match, so the 5 rows before it are thrown away
assert ids.index(106) == 5
# first page of the real shop has all 7 orders, delivered is 5, so 2 removed
assert q("SELECT count(*) FROM orders WHERE status <> 'delivered'") == [(2,)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'") == [(5,)]
assert q("SELECT count(*) FROM orders") == [(7,)]
# 800 pages in check yourself 1 is made up, 3 cancelled orders is not a shop fact
# run on a real Postgres 16 server, copy of orders without a primary key (orders1000,
# 1000 rows from generate_series, 8 pages): EXPLAIN (ANALYZE, BUFFERS) gave
#  Seq Scan, Rows Removed by Filter 999, Buffers shared hit=8 for order_id = 106
#  Rows Removed 1000, shared hit=8 for order_id = 999999
#  Limit over Seq Scan, Rows Removed 5, shared hit=1 with LIMIT 1
# the 7 order table with a PRIMARY KEY still gave Seq Scan, Rows Removed 6, hit=1 for 106
# a 100000 row table of the same 4 column shape (136 rows per page, as in 286) had pg_relation_size
# 6029312 bytes, 736 pages, audit rerun on Postgres 16.15; 640 pages was wrong for this shape
assert -(-100000 // 136) == 736 and 736 * 8192 == 6029312
# source: https://www.postgresql.org/docs/16/using-explain.html
#   confirmed: a query with no WHERE uses a sequential scan of all rows, Rows Removed by Filter
#   is shown for a filter, and the planner skips an index on a tiny table (polygon_tbl example)
# source: https://www.postgresql.org/docs/16/sql-explain.html
#   confirmed: BUFFERS counts shared blocks hit, and a hit means the block was found in cache
# source: https://www.postgresql.org/docs/16/runtime-config-compatible.html
#   confirmed: synchronize_seqscans (default on) lets a scan of a large table start in the middle and wrap around, so the order is not always first page to last
