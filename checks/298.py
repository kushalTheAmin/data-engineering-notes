# checks for notes/298-nested-loop-join-for-each-outer-row-search-the-inner-side.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server: orders100k (order_id 101..100100, customer_id = order_id % 5 + 1), customers (the 5 shop customers),
# primary keys on both ids, VACUUM ANALYZE. plain EXPLAIN for order_id = 500:
# Nested Loop cost=0.29..9.42 rows=1, Index Scan using orders100k_pkey (outer), Seq Scan on customers rows=5 (inner), Join Filter customer_id
# with enable_nestloop off the same query is a Hash Join cost=1.41..9.43
# no WHERE: Hash Join cost=1.11..2126.11; with enable_hashjoin and enable_mergejoin off: Nested Loop cost=0.14..3940.88 (inner is a Memoize over an Index Scan using customers_pkey)
assert 9.42 < 9.43 and round(9.43 - 9.42, 2) == 0.01 and 3940.88 > 2126.11
assert 500 % 5 + 1 == 1 and q("SELECT name FROM customers WHERE customer_id = 1") == [("Asha",)]
assert 1 * 5 == 5
# 20000 of the made up orders belong to one customer (customer_id 5)
assert sum(1 for g in range(101, 100101) if g % 5 + 1 == 5) == 20000 and 20000 * 5 == 100000
assert q("SELECT o.order_id, c.name FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled'") == [(104, "Chirag")]
assert q("SELECT count(*) FROM customers")[0][0] == 5 and q("SELECT count(*) FROM orders")[0][0] * 5 == 35
# source: https://www.postgresql.org/docs/16/planner-optimizer.html
#   confirmed: nested loop join scans the right relation once for every row found in the left relation, and an index scan on the right can make it a good strategy (opened this run)
# source: https://www.postgresql.org/docs/16/planner-optimizer.html
#   confirmed: hash join - the right relation is first scanned and loaded into a hash table, then the left relation is scanned and its values used as hash keys to locate the matching rows in the table (opened this run)
# audit: the note used hash join in its table with no explanation, so it now glosses it
# audit: to stay under 250 words the sentence both costs grow with the outer rows was dropped, the table already shows 9.42 against 3940.88 and 9.43 against 2126.11
