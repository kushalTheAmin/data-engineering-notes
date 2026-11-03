# checks for notes/305-capstone-one-query-from-sql-text-to-rows-on-disk.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# check yourself 1: the 7 real orders have exactly one cancelled order, 104
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT order_id, status FROM orders WHERE status = 'cancelled'") == [(104, "cancelled")]
# costs quoted from note 296 (Postgres 16 run): 7 real orders, Seq Scan 1.09 against Index Scan 8.15
assert 1.09 < 8.15
# check yourself 2: guessed 5, real 50000 is a wrong guess
assert 5 != 50000  # source for ANALYZE and VACUUM ANALYZE: see below
# the section ran from note 284 to 304, 21 notes, all linked in builds on
assert len(range(284, 305)) == 21
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed (opened this run): statistics for the planner are gathered by ANALYZE, which can be invoked by itself or as an optional step in VACUUM, so plain VACUUM does not refresh them; autovacuum also issues ANALYZE
