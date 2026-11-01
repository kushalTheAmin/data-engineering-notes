# checks for notes/296-the-query-planner-picking-the-cheapest-plan.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server: orders100k (order_id 101..100100, status cancelled when order_id % 1000 = 0 else delivered),
# index on status, VACUUM ANALYZE. 736 table pages. plain EXPLAIN (no ANALYZE):
# cancelled: Index Scan cost=0.29..14.36 rows=137. delivered: Seq Scan cost=0.00..1986.00 rows=99863
# with enable_seqscan = off, delivered: Index Scan cost=0.29..2849.71. cancelled with indexscan and bitmapscan off: Seq Scan 0.00..1986.00
# the 7 real orders (copy with primary key and index on status): cancelled Seq Scan cost=0.00..1.09, with enable_seqscan off Index Scan cost=0.13..8.15
assert round(736 * 1.0 + 100000 * (0.01 + 0.0025), 2) == 1986.00
assert 14.36 < 1986.00 < 2849.71 and 1.09 < 8.15
assert 100100 // 1000 - 100 // 1000 == 100 and 137 != 100 and 99863 + 137 == 100000
assert q("SELECT order_id FROM orders WHERE status = 'cancelled'") == [(104,)]
assert q("SELECT order_id FROM orders WHERE status = 'delivered' ORDER BY order_id") == [(101,), (102,), (103,), (105,), (107,)]
assert 7 <= 136  # 7 rows fit on one page, 136 rows per page as in 284 to 286
# source: https://www.postgresql.org/docs/16/using-explain.html
#   confirmed: costs are in arbitrary units set by the planner's cost parameters, traditionally disk page fetches, with seq_page_cost 1.0 (opened this run)
# source: https://www.postgresql.org/docs/16/runtime-config-query.html
#   confirmed: cpu_tuple_cost default 0.01, cpu_operator_cost default 0.0025; enable_seqscan off discourages sequential scans, it cannot suppress them entirely (opened this run)
# audit of draft: the 1986 Seq Scan cost holds for these two single-condition WHEREs; the SELECT order_id shape (not count(*)) is what the 14.36 and 2849.71 costs belong to
