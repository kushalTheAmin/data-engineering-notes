# checks for notes/287-b-tree-pages-that-point-to-pages.md
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# a balanced binary tree of 1000 orders: about 10 looks (2**10 = 1024 >= 1001)
assert math.ceil(math.log2(1001)) == 10
# the 1000 made up orders of 286, ids 101 to 1100, split by the real Postgres 16 leaves
assert 1100 - 101 + 1 == 1000
leaves = [(101, 466), (467, 832), (833, 1100)]
sizes = [b - a + 1 for a, b in leaves]
assert sizes == [366, 366, 268] and sum(sizes) == 1000
# root signposts 467 and 833: 2 signposts, 3 children, n signposts -> n + 1 children
assert len(leaves) == 2 + 1
# the 5 index pages of 286: 1 root + 3 leaves + 1 metapage
assert 1 + 3 + 1 == 5
# run on a real Postgres 16.15 server: orders1000 = generate_series(101,1100), CREATE INDEX on order_id.
# pg_relation_size of the index 5 pages; bt_metap level 1 root block 3; bt_page_items of the root shows 3 items,
# the first with no value and downlinks to blocks 1, 2, 4 with values 467 (0x01d3) and 833 (0x0341);
# bt_page_stats: blocks 1, 2 and 4 are leaves with 367, 367, 268 live items, and the first two include
# 1 high key each, so 366, 366 and 268 real entries (101 to 466, 467 to 832, 833 to 1100)
# check yourself 1: the toy root with signposts 104 and 107 over orders 101 to 107
assert q("SELECT order_id FROM orders ORDER BY order_id") == [(i,) for i in range(101, 108)]
assert q("SELECT order_id FROM orders WHERE order_id >= 104 AND order_id < 107 ORDER BY order_id") == [(104,), (105,), (106,)]
# leaves of at most 3: 101-103, 104-106, 107
ids = list(range(101, 108))
assert [ids[i:i + 3] for i in range(0, 7, 3)] == [[101, 102, 103], [104, 105, 106], [107]]
# check yourself 2
assert 299 + 1 == 300 and 300 * 300 == 90000 and 299 * 300 == 89700
# source: https://www.postgresql.org/docs/16/btree-implementation.html
#   confirmed: B-Tree indexes are multi-level trees, internal pages hold tuples pointing to the next level down,
#   leaf pages hold tuples pointing to table rows, a single metapage sits at the start, and typically over 99% of pages are leaf pages
