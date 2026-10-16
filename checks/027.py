# checks for notes/027-dates-and-times-apart.md
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
from datetime import datetime, date
con = shop()
rows = con.sql("SELECT order_id, ordered_at::DATE, ordered_at::TIME FROM orders WHERE order_id IN (101, 102, 103) ORDER BY 1").fetchall()
assert [(r[0], str(r[1]), str(r[2])) for r in rows] == [(101, "2026-04-01", "09:15:00"), (102, "2026-04-01", "18:40:00"), (103, "2026-04-03", "12:05:00")]
assert con.sql("SELECT count(*) FROM orders WHERE ordered_at <= DATE '2026-04-01'").fetchone()[0] == 0
assert con.sql("SELECT count(*) FROM orders WHERE ordered_at::DATE <= DATE '2026-04-01'").fetchone()[0] == 2
# a date compared with a timestamp becomes midnight of that day
assert con.sql("SELECT TIMESTAMP '2026-04-01 09:15:00' > DATE '2026-04-01'").fetchone()[0] is True
assert con.sql("SELECT DATE '2026-04-01' = TIMESTAMP '2026-04-01 00:00:00'").fetchone()[0] is True
assert str(con.sql("SELECT joined_on FROM customers WHERE customer_id = 1").fetchone()[0]) == "2026-01-05"
# orders 101 and 102 are the two on 1 April
assert [r[0] for r in con.sql("SELECT order_id FROM orders WHERE ordered_at::DATE = DATE '2026-04-01' ORDER BY 1").fetchall()] == [101, 102]
print("027 ok")
