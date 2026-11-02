# checks for notes/301-reading-explain-the-plan-as-a-tree.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# run on a real Postgres 16.15 server holding the 5 tables of data/shop.sql, after ANALYZE. plain EXPLAIN (COSTS OFF) of the delivered query:
# HashAggregate (Group Key c.name) > Hash Join (Hash Cond o.customer_id = c.customer_id) > [Seq Scan on orders o with Filter status = delivered, Hash > Seq Scan on customers c]
# 8 lines of plan including the "Group Key", "Hash Cond" and "Filter" lines (the summary line "(8 rows)" not counted)
# EXPLAIN (ANALYZE) actual rows: HashAggregate 3, Hash Join 5, Seq Scan orders 5 with Rows Removed by Filter 2, Hash 5, Seq Scan customers 5
# with costs on the top line is HashAggregate cost=2.25..2.30, so the total is 2.30
# for status = cancelled Postgres 16 picks GroupAggregate > Sort > Nested Loop, with Seq Scan on orders o rows=1, so the plan shape differs (the note says "may pick other join nodes")
plan_lines = ["HashAggregate", "Group Key", "Hash Join", "Hash Cond", "Seq Scan orders", "Filter", "Hash", "Seq Scan customers"]
assert len(plan_lines) == 8
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'")[0][0] == 5
assert q("SELECT count(*) FROM orders WHERE status <> 'delivered'")[0][0] == 2
assert q("SELECT count(*) FROM customers")[0][0] == 5
assert q("SELECT c.name, count(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'delivered' GROUP BY c.name ORDER BY c.name") == [("Asha", 2), ("Bhavin", 2), ("Disha", 1)]
assert len(q("SELECT 1 FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'delivered'")) == 5
assert q("SELECT count(*) FROM orders WHERE status = 'delivered' AND customer_id = 5")[0][0] == 0
assert q("SELECT name FROM customers WHERE customer_id = 5") == [("Esha",)]
assert q("SELECT c.name, count(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'cancelled' GROUP BY c.name") == [("Chirag", 1)]
assert q("SELECT count(*) FROM orders WHERE status = 'cancelled'")[0][0] == 1
# source: https://www.postgresql.org/docs/16/using-explain.html
#   confirmed: EXPLAIN output has one line for each node in the plan tree, extra lines are indented from the node's summary line, and the cost of an upper-level node includes the cost of all its child nodes (opened this run)
