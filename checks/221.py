# checks for notes/221-insert-from-a-select-copying-rows-from-a-query.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, 5 delivered, 104 cancelled, 106 pending
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT order_id, status FROM orders WHERE status <> 'delivered' ORDER BY 1") == [(104, "cancelled"), (106, "pending")]
con.execute("CREATE TABLE delivered (order_id INTEGER, customer_id INTEGER, ordered_at TIMESTAMP)")
ins = "INSERT INTO delivered SELECT order_id, customer_id, ordered_at FROM orders WHERE status = 'delivered'"
con.execute(ins)
dt = datetime.datetime
assert q("SELECT * FROM delivered ORDER BY order_id") == [
    (101, 1, dt(2026, 4, 1, 9, 15)), (102, 2, dt(2026, 4, 1, 18, 40)), (103, 1, dt(2026, 4, 3, 12, 5)),
    (105, 4, dt(2026, 4, 6, 19, 10)), (107, 2, dt(2026, 4, 9, 13, 45))]
con.execute(ins)
assert q("SELECT count(*), count(DISTINCT order_id) FROM delivered") == [(10, 5)]
# a swapped column order still loads, both are whole numbers
con.execute("CREATE TABLE swapped (order_id INTEGER, customer_id INTEGER, ordered_at TIMESTAMP)")
con.execute("INSERT INTO swapped SELECT customer_id, order_id, ordered_at FROM orders WHERE status = 'delivered'")
assert q("SELECT count(*) FROM swapped") == [(5,)]
# a primary key on order_id refuses the second run
con.execute("CREATE TABLE keyed (order_id INTEGER PRIMARY KEY, customer_id INTEGER, ordered_at TIMESTAMP)")
k = ins.replace("delivered SELECT", "keyed SELECT")
con.execute(k)
try:
    con.execute(k)
    assert False
except Exception as e:
    assert "Constraint" in str(e) or "duplicate" in str(e).lower()
assert q("SELECT count(*) FROM keyed") == [(5,)]
# source: https://www.postgresql.org/docs/current/sql-insert.html
#   confirmed (opened this run): "One can insert one or more rows specified by value expressions, or zero or more rows resulting from a query"; query values are associated with the column list left-to-right.
