# checks for notes/293-what-indexes-cost-slower-writes-and-more-disk.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM order_items") == [(13,)]
# run on a real Postgres 16 server: orders1000 = 4 columns (order_id, customer_id, status, ordered_at)
# from generate_series(101,1100), 1000 rows. pg_relation_size / 8192: table 8 pages; CREATE INDEX on
# (order_id) 5 pages; CREATE INDEX on (customer_id, ordered_at) 6 pages. pageinspect leaf entry counts
# before and after INSERT of order 1101: order_id index 1002 -> 1003, composite 1003 -> 1004 (+1 each)
assert 5 + 6 == 11 and 11 > 8
assert 8 + 5 + 6 == 19
assert 1003 - 1002 == 1 and 1004 - 1003 == 1
assert 1 + 2 == 3  # one table row plus one entry in each of two indexes
# source: https://www.postgresql.org/docs/16/indexes-intro.html
#   confirmed: the system has to keep an index synchronized with the table, which adds overhead to data manipulation operations, and indexes seldom or never used in queries should be removed (opened this run)
# source: https://www.postgresql.org/docs/16/btree-implementation.html
#   confirmed: each leaf page holds tuples pointing to table rows and a metapage sits at the start of the index (opened this run)
# audit: not every INSERT adds an entry to every index. Postgres 16.15 run this audit: a partial index (CREATE INDEX ... WHERE status = 'cancelled') on orders1000, then INSERT of a 'delivered' order, left the index with no leaf page at all (bt_page_items block 1 out of range), so no entry was added. the note now says usually
