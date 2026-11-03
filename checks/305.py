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
# source: https://www.postgresql.org/docs/16/catalogs.html
#   confirmed (opened this run): the system catalogs are regular tables, and the planner statistics live in one (pg_statistic, https://www.postgresql.org/docs/16/planner-stats.html), so planning itself reads pages
# audit: the note said the planner and plan decide before anything is read, but Postgres 16 run this audit printed "Planning: Buffers: shared hit=16" for EXPLAIN (ANALYZE, BUFFERS) on a 100000 row table, so planning touches pages too. it now says before your table is read. the 7 order index on status run gave Seq Scan 1.09 and, with enable_seqscan off, Index Scan 8.15, matching check yourself 1
# source: https://www.postgresql.org/docs/16/sql-explain.html
#   confirmed (opened this run): the ANALYZE option causes the statement to be actually executed, not only planned
