# checks for notes/302-explain-analyze-the-planners-guesses-vs-what-really-happened.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server: customers (the 5 shop customers), orders100k (order_id 101..100100, customer_id = order_id % 5 + 1,
# status cancelled when order_id % 1000 = 0, pending when order_id % 10 = 1, else delivered), primary keys, index on status, VACUUM ANALYZE.
# EXPLAIN ANALYZE of cancelled orders per customer (run 2 of 3, shown in the note):
# HashAggregate cost=118.76..118.81 rows=5 actual time=0.622..0.625 rows=1 / Hash Join cost=1.41..118.31 rows=90 actual rows=100
# / Index Scan using orders100k_status_idx cost=0.29..116.76 rows=90 actual time=0.019..0.549 rows=100 / Hash rows=5 actual rows=5 / Seq Scan on customers rows=5 actual rows=5
# Execution Time: 0.709 ms (varied 0.66 to 1.00 ms over 3 runs; the rows numbers were the same every run)
# real orders cancelled when order_id % 1000 = 0: 100, all with customer_id 1 (Asha)
ids = [g for g in range(101, 100101) if g % 1000 == 0]
assert len(ids) == 100
assert {g % 5 + 1 for g in ids} == {1}
assert q("SELECT name FROM customers WHERE customer_id = 1") == [("Asha",)]
assert 100 - 90 == 10 and 5 != 1
# check yourself 1: UPDATE of Ashas orders (customer 1) to cancelled, plus Chirags 104 already cancelled, gives 4
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT count(*) AS cancelled FROM orders WHERE status = 'cancelled'") == [(1,)]  # before the UPDATE
con2 = shop()
con2.execute("UPDATE orders SET status = 'cancelled' WHERE customer_id = 1")
assert con2.execute("SELECT count(*) AS cancelled FROM orders WHERE status = 'cancelled'").fetchall() == [(4,)]  # after: what the note shows
# audit: the old query had OR customer_id = 1 and returned 4 before and after the UPDATE, so it could not show whether ANALYZE ran the update
assert q("SELECT count(*) FROM orders WHERE customer_id = 1")[0][0] == 3
assert q("SELECT order_id, name FROM orders o JOIN customers c USING (customer_id) WHERE status = 'cancelled'") == [(104, "Chirag")]
# Postgres 16.15 run: EXPLAIN ANALYZE DELETE on a 7 row copy, then SELECT count(*) returned 6 (so ANALYZE really applies writes; note uses an UPDATE because real shop orders have child rows that block a DELETE)
# check yourself 2
assert 2000 / 2 == 1000
# source: https://www.postgresql.org/docs/16/using-explain.html
#   confirmed: with ANALYZE, EXPLAIN actually executes the query and shows true row counts and run time per node; actual time is in milliseconds of real time while costs are arbitrary units;
#   the most important thing to look for is whether estimated row counts are close to reality; INSERT/UPDATE/DELETE are really applied, so wrap in BEGIN ... ROLLBACK (opened this run)
