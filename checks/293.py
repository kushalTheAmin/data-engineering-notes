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
#   confirmed: "After an index is created, the system has to keep it synchronized with the table. This adds overhead to data manipulation operations." and, in a separate paragraph, "Indexes can also prevent the creation of heap-only tuples. Therefore indexes that are seldom or never used in queries should be removed." (opened this run)
# audit: the old note joined the two with since, but the docs give heap-only tuples as the reason for removal, so the note now states the two facts separately
# source: https://www.postgresql.org/docs/16/btree-implementation.html
#   confirmed: each leaf page holds tuples pointing to table rows and a metapage sits at the start of the index (opened this run)
# audit: not every INSERT adds an entry to every index. Postgres 16.15 run this audit: a partial index (CREATE INDEX ... WHERE status = 'cancelled') on orders1000, then INSERT of a 'delivered' order, left the index with no leaf page at all (bt_page_items block 1 out of range), so no entry was added. the note now says usually
# audit: Postgres 16.15 run this audit on a 1000 row copy (4 columns): heap_page_items lp_len 56 for every row (136 per page), bt_page_items itemlen 16 (order_id index) and 24 (composite), bt_page_stats: order_id index = metapage + root + 3 leaf pages, composite = metapage + root + 4 leaf pages
assert 3 + 4 == 7 and 7 + 2 * 2 == 11
assert 16 < 24 < 56
# source: https://www.postgresql.org/docs/16/indexes-unique.html
#   confirmed: PostgreSQL automatically creates a unique index when a unique constraint or primary key is defined for a table (opened this run)
# audit: metapage and root page are now glossed in the note. source above (btree-implementation): a single metapage is stored at the start of the index, leaf pages are the lowest level and all other levels are internal pages
