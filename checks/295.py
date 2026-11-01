# checks for notes/295-functions-on-a-column-why-the-index-gets-skipped.md
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server: orders100k (order_id, customer_id, ordered_at, status text), 100000 rows
# order_id 101+i, ordered_at = 2025-01-01 + i * 10 minutes, indexes on ordered_at and on order_id, VACUUM ANALYZE.
# pg_relation_size / 8192 = 736 table pages, 276 pages in the ordered_at index
assert 24 * 60 // 10 == 144 and math.ceil(100000 / 136) == 736
# CAST(ordered_at AS DATE) = '2025-06-01': count 144, Seq Scan, Rows Removed 99856, Buffers shared hit=736
assert 144 + 99856 == 100000
# range form: Index Scan, rows=144, Buffers shared hit=2 read=2 -> 4 pages
assert 2 + 2 == 4 and 736 > 4
# order_id + 1 = 5001 with an index on order_id: Seq Scan, hit=736. order_id = 5000: Index Only Scan, hit=1 read=2 -> 3 pages
assert 1 + 2 == 3  # all 3 were index pages (Index Only Scan)
# 2025-06-01 is day 151 of 2025 counting from 0 (31+28+31+30+31), first row index 151*144 < 100000
assert 31 + 28 + 31 + 30 + 31 == 151 and 151 * 144 + 144 < 100000
# the 7 real orders, range form and CAST form give the same rows
assert q("SELECT order_id FROM orders WHERE ordered_at >= TIMESTAMP '2026-04-01' AND ordered_at < TIMESTAMP '2026-04-02' ORDER BY order_id") == [(101,), (102,)]
assert q("SELECT order_id FROM orders WHERE CAST(ordered_at AS DATE) = DATE '2026-04-01' ORDER BY order_id") == [(101,), (102,)]
assert q("SELECT order_id FROM orders WHERE order_id + 1 = 108") == [(107,)]
assert q("SELECT customer_id FROM customers WHERE lower(name) = 'asha'") == [(1,)]
# Postgres 16.15 on cust100k (100000 names like Asha6) with index on name: lower(name) = 'asha6' was a Seq Scan,
# after CREATE INDEX ON cust100k (lower(name)) it was an Index Scan
# source: https://www.postgresql.org/docs/16/indexes-expressional.html
#   confirmed: a lower(col1) query can use an index defined on lower(col1), and index expressions are relatively expensive to maintain because they are computed on each row insertion (opened this run)
# audit: the docs say index expressions are computed for each row insertion and non-HOT update, so the note says most updates, not every update
# source: https://www.postgresql.org/docs/16/indexes-expressional.html
#   confirmed: "Index expressions are relatively expensive to maintain, because the derived expression(s) must be computed for each row insertion and non-HOT update" (opened this run)
