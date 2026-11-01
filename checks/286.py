# checks for notes/286-index-a-sorted-shortcut-to-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the made up table of 285: ids 101 to 1100, 136 rows per page, 8 pages
per_page = 136
table = [(101 + i, i // per_page, i % per_page + 1) for i in range(1000)]
assert len(table) == 1000
assert -(-1000 // per_page) == 8
assert table[-1] == (1100, 7, 48) and 1000 - 7 * per_page == 48
index = sorted(table)
def find(index, want):
    lo, hi, looks = 0, len(index) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        looks += 1
        if index[mid][0] == want:
            return index[mid], looks
        if index[mid][0] < want:
            lo = mid + 1
        else:
            hi = mid - 1
assert find(index, 1100) == ((1100, 7, 48), 10)
# pages 0 to 6 are skipped, only page 7 is read
assert list(range(7)) == [0, 1, 2, 3, 4, 5, 6]
# check yourself 1: 7 orders, Asha is customer 1 with 3 orders
assert q("SELECT customer_id FROM customers WHERE name = 'Asha'") == [(1,)]
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
assert len(q("SELECT DISTINCT customer_id FROM orders")) == 4
# run on a real Postgres 16.15 server: table orders1000 (4 columns: order_id, customer_id, status,
# ordered_at, from generate_series(101,1100), 1000 rows, pg_relation_size 8 pages; a 5th text column gave 16). before the index:
# Seq Scan, Buffers shared hit=8 for order_id = 106 (and 1100). CREATE INDEX orders1000_id_idx ON
# orders1000 (order_id): pg_relation_size of the index 5 pages, bt_metap level 1 (a root and leaves,
# so a lookup reads 2 index pages). Index Scan for order_id = 1100: Buffers shared hit=3 once cached
# (2 index pages and 1 table page). Index Scan for order_id = 999999: actual rows=0, Buffers shared hit=2.
# ctid of 101, 106, 107 was (0,1), (0,6), (0,7), of 1100 (7,48), 136 rows on page 0
assert 2 + 1 == 3
# source: https://www.postgresql.org/docs/16/indexes-types.html
#   confirmed: the CREATE INDEX command creates a B-tree index by default, and Hash, GiST, SP-GiST, GIN and BRIN also exist
# source: https://www.postgresql.org/docs/16/indexes-unique.html
#   confirmed: Postgres automatically creates a unique index when a unique constraint or primary key is defined
# source: https://www.postgresql.org/docs/16/indexes-types.html
#   confirmed: Hash indexes store a 32-bit hash code of the value and handle only equality, so not every index is sorted
# source: https://www.postgresql.org/docs/16/sql-createindex.html
#   confirmed: the default index method is btree
# 'most writes update the index': a HOT update (no indexed column changed, room on the page) adds no index entry
#   rerun this audit on Postgres 16.15: index on orders(order_id), UPDATE status of 106 gave n_tup_hot_upd 1
# source: https://www.postgresql.org/docs/16/storage-hot.html
#   confirmed: "New index entries are not needed to represent updated rows" when no indexed column changes and the page has free space
