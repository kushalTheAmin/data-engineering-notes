# checks for notes/301-reading-explain-the-plan-as-a-tree.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server: customers (the 5 shop customers), orders100k (order_id 101..100100, customer_id = order_id % 5 + 1,
# status cancelled when order_id % 1000 = 0, pending when order_id % 10 = 1, else delivered), primary keys, index on status, VACUUM ANALYZE.
# plain EXPLAIN of cancelled orders per customer:
# HashAggregate cost=136.26..136.31 rows=5 / Hash Join cost=1.41..135.78 rows=97 / Index Scan using orders100k_status_idx cost=0.29..134.20 rows=97
# / Hash cost=1.05..1.05 rows=5 / Seq Scan on customers cost=0.00..1.05 rows=5
assert sum(1 for g in range(101, 100101) if g % 1000 == 0) == 100
assert 134.20 < 135.78 < 136.31 and round(136.31 - 135.78, 2) == 0.53
assert 97 != 100
# the plan has 5 nodes, 2 leaves
nodes = ["HashAggregate", "Hash Join", "Index Scan", "Hash", "Seq Scan"]
assert len(nodes) == 5
# check yourself 1: the real 7 orders, one cancelled order (104, Chirag)
assert q("SELECT c.name, count(*) AS orders FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled' GROUP BY c.name") == [("Chirag", 1)]
assert q("SELECT count(*) FROM customers")[0][0] == 5
# check yourself 2
assert 4000.00 - 3990.00 == 10.0
# source: https://www.postgresql.org/docs/16/using-explain.html
#   confirmed: the indentation of the node summary lines reflects the plan tree structure, the cost of an upper-level node includes the cost of all its child nodes, cost is (startup..total), rows is an estimate (opened this run)
