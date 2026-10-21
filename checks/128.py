# checks for notes/128-adding-and-subtracting-intervals.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
D = datetime.datetime
rows = q("SELECT order_id, ordered_at, ordered_at + INTERVAL 2 DAY FROM orders WHERE order_id IN (101, 102, 103, 107) ORDER BY order_id")
assert rows == [
    (101, D(2026, 4, 1, 9, 15), D(2026, 4, 3, 9, 15)),
    (102, D(2026, 4, 1, 18, 40), D(2026, 4, 3, 18, 40)),
    (103, D(2026, 4, 3, 12, 5), D(2026, 4, 5, 12, 5)),
    (107, D(2026, 4, 9, 13, 45), D(2026, 4, 11, 13, 45)),
]
for oid, a, b in rows:
    assert b - a == datetime.timedelta(days=2)
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT DATE '2026-01-31' + INTERVAL 1 MONTH, DATE '2026-01-31' + INTERVAL 30 DAY") == [(D(2026, 2, 28), D(2026, 3, 2))]
# python agrees on the 30 days; timedelta has no months at all
assert datetime.date(2026, 1, 31) + datetime.timedelta(days=30) == datetime.date(2026, 3, 2)
try:
    datetime.timedelta(months=1)
    assert False
except TypeError:
    pass
assert q("SELECT typeof(DATE '2026-01-31' + INTERVAL 1 MONTH)") == [("TIMESTAMP",)]
assert q("SELECT ordered_at - INTERVAL 3 HOUR FROM orders WHERE order_id = 101") == [(D(2026, 4, 1, 6, 15),)]
assert q("SELECT ordered_at + INTERVAL '2 days' FROM orders WHERE order_id = 101") == [(D(2026, 4, 3, 9, 15),)]
assert q("SELECT DATE '2026-03-31' + INTERVAL 1 MONTH") == [(D(2026, 4, 30),)]
assert q("SELECT count(*) FROM orders WHERE ordered_at > TIMESTAMP '2026-04-09 14:00:00' - INTERVAL 3 DAY") == [(3,)]
assert q("SELECT TIMESTAMP '2026-04-09 14:00:00' - INTERVAL 3 DAY") == [(D(2026, 4, 6, 14),)]
assert q("SELECT order_id FROM orders WHERE ordered_at > TIMESTAMP '2026-04-06 14:00:00' ORDER BY 1") == [(105,), (106,), (107,)]
assert q("SELECT ordered_at FROM orders WHERE order_id = 105") == [(D(2026, 4, 6, 19, 10),)]
assert q("SELECT (DATE '2026-01-31' + INTERVAL 1 MONTH) - INTERVAL 1 MONTH") == [(D(2026, 1, 28),)]
# source: https://duckdb.org/docs/current/sql/data_types/interval
# confirmed: "a month does not correspond to a fixed amount of days (February has fewer days than March)"; INTERVAL '1 month 1 day' string form is accepted
# source: https://duckdb.org/docs/current/sql/functions/date
# confirmed: DATE '1992-03-22' + INTERVAL 5 DAY gives 1992-03-27 00:00:00, so date plus interval is a timestamp
# source: https://www.postgresql.org/docs/current/functions-datetime.html
# confirmed: Postgres examples use quoted intervals, e.g. date '2001-09-28' + interval '1 hour'
# source: https://docs.python.org/3/library/datetime.html
# confirmed: timedelta takes days, seconds, microseconds, milliseconds, minutes, hours, weeks (no months)
