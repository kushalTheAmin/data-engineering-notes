# checks for notes/265-created-at-and-updated-at-two-timestamps-every-table-carries.md
import os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT order_id, status, created_at, updated_at FROM order_tracking WHERE order_id IN (104, 105, 106) ORDER BY order_id") == [
    (104, "cancelled", datetime(2026, 4, 4, 8, 30), datetime(2026, 4, 4, 8, 45)),
    (105, "delivered", datetime(2026, 4, 6, 19, 10), datetime(2026, 4, 6, 20, 15)),
    (106, "pending", datetime(2026, 4, 8, 10, 0), datetime(2026, 4, 8, 10, 0)),
]
# 104 was cancelled 15 minutes after it was placed
assert q("SELECT date_diff('minute', created_at, updated_at) FROM order_tracking WHERE order_id = 104") == [(15,)]
# the tracking table agrees with orders on creation time and status
assert q("SELECT count(*) FROM order_tracking t JOIN orders o USING (order_id) WHERE o.ordered_at = t.created_at AND o.status = t.status") == [(7,)]
# only 106 has equal times
assert q("SELECT order_id FROM order_tracking WHERE updated_at = created_at") == [(106,)]
# question 1
assert q("SELECT order_id FROM order_tracking WHERE updated_at > TIMESTAMP '2026-04-06 00:00:00' ORDER BY order_id") == [(105,), (106,), (107,)]
# question 2: an UPDATE that does not SET updated_at leaves it alone
con.execute("UPDATE order_tracking SET status = 'delivered' WHERE order_id = 106")
assert q("SELECT status, updated_at FROM order_tracking WHERE order_id = 106") == [("delivered", datetime(2026, 4, 8, 10, 0))]
# DEFAULT current_timestamp fills both columns on insert
con.execute("CREATE TABLE t (id INTEGER, created_at TIMESTAMP NOT NULL DEFAULT current_timestamp, updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp)")
con.execute("INSERT INTO t (id) VALUES (1)")
assert q("SELECT created_at = updated_at FROM t") == [(True,)]
# source: https://dev.mysql.com/doc/refman/8.0/en/timestamp-initialization.html
# confirmed: MySQL column definitions can use DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP as automatic properties
# source: https://www.postgresql.org/docs/current/trigger-definition.html
# confirmed: a Postgres trigger makes the database automatically execute a function whenever an INSERT, UPDATE or DELETE happens on a table
