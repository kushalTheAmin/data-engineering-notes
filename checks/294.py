# checks for notes/294-selectivity-when-an-index-doesnt-help.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the 7 real orders: 5 delivered, 1 cancelled, 1 pending
assert q("SELECT status, count(*) FROM orders GROUP BY status ORDER BY status") == [("cancelled", 1), ("delivered", 5), ("pending", 1)]
assert round(100 * 5 / 7) == 71 and round(100 * 1 / 7) == 14
# run on a real Postgres 16.15 server: orders100k, 100000 rows from generate_series(101,100100),
# columns order_id, customer_id, status, ordered_at; status cancelled when order_id % 1000 = 0
# (100 rows), else delivered (99900); CREATE INDEX on (status); VACUUM ANALYZE.
# pg_relation_size / 8192 = 768 table pages, 88 index pages. the 100 cancelled rows sit on 100 distinct pages.
# EXPLAIN (ANALYZE, BUFFERS) cancelled: Index Scan, rows=100, shared hit=100 read=2 (102)
# delivered: Seq Scan, rows=99900, Rows Removed 100, shared hit=768
# delivered with enable_seqscan = off: Index Scan, hit=738 read=85 (823)
assert 100 + 2 == 102 and 738 + 85 == 823 and 823 > 768
assert 100 + 99900 == 100000 and 100 / 100000 == 0.001 and 99900 / 100000 == 0.999
# check yourself 1: 99.8 percent of 100000 is true
assert 100000 * 998 // 1000 == 99800 and 100000 - 99800 == 200
# check yourself 2: o7, 100000 rows in the 5:1:1 mix (order_id % 7 = 3 cancelled, 5 pending), 768 pages
# counts: cancelled 14286, delivered 71428, pending 14286. delivered: Seq Scan hit=768.
# pending: Bitmap Heap Scan, Heap Blocks exact=725, Bitmap Index Scan read=14 -> 725 + 14 = 739
assert 14286 + 71428 + 14286 == 100000 and round(100 * 14286 / 100000) == 14
assert 725 + 14 == 739 and 739 < 768 and round(0.14286 * 768) == 110
# note: Buffers counts page visits, so 823 can exceed the 768 pages of the table. in o7 the pending plan was chosen by the planner (Bitmap Heap Scan), not forced
