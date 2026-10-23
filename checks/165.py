# checks for notes/165-double-counting-why-sums-after-a-fan-out-lie.md
import os, sys
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT sum(fee) FROM order_fees") == [(D("15.00"),)]
assert q("SELECT sum(f.fee), count(*), sum(DISTINCT f.fee) FROM order_fees f JOIN order_items oi ON f.order_id = oi.order_id") == [(D("31.00"), 13, D("5.00"))]
assert 31 - 15 == 16
assert q("SELECT f.order_id, f.fee, oi.product_id FROM order_fees f JOIN order_items oi ON f.order_id = oi.order_id WHERE f.order_id IN (104, 105) ORDER BY 1, 3") == [(104, D("0.00"), 1), (105, D("3.00"), 3), (105, D("3.00"), 4), (105, D("3.00"), 5)]
assert q("SELECT DISTINCT fee FROM order_fees ORDER BY 1") == [(D("0.00"),), (D("2.00"),), (D("3.00"),)] and 0 + 2 + 3 == 5
# by hand: each fee times its item count
items = dict(q("SELECT order_id, count(*) FROM order_items GROUP BY 1"))
fees = dict(q("SELECT order_id, fee FROM order_fees"))
assert sum(fees[o] * items[o] for o in fees) == D("31.00")
# Asha: orders 101, 103, 106 with fee 2.00 and 2, 2, 1 items
assert q("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY 1") == [(101,), (103,), (106,)]
assert [items[o] for o in (101, 103, 106)] == [2, 2, 1] and 2 + 2 + 1 == 5 and 5 * 2 == 10 and 3 * 2 == 6
a = "FROM orders o JOIN order_fees f ON o.order_id = f.order_id JOIN order_items oi ON o.order_id = oi.order_id WHERE o.customer_id = 1"
assert q("SELECT sum(f.fee) " + a) == [(D("10.00"),)]
assert q("SELECT sum(DISTINCT f.fee) " + a) == [(D("2.00"),)]
# 7 fees in total, and summing a many side column in this join is safe: quantity totals 20 either way
assert q("SELECT count(*) FROM order_fees") == [(7,)]
assert q("SELECT sum(oi.quantity) FROM order_fees f JOIN order_items oi ON f.order_id = oi.order_id") == q("SELECT sum(quantity) FROM order_items") == [(20,)]
# source: https://duckdb.org/docs/2.0/sql/functions/aggregates.html
# confirmed: "When the DISTINCT clause is provided, only distinct values are considered in the computation of the aggregate."
