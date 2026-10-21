# checks for notes/127-truncating-timestamps-to-a-day-or-a-month.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
D = datetime.datetime
rows = q("SELECT order_id, ordered_at, date_trunc('day', ordered_at), date_trunc('month', ordered_at) FROM orders WHERE order_id IN (101, 102, 103, 107) ORDER BY order_id")
assert rows == [
    (101, D(2026, 4, 1, 9, 15), D(2026, 4, 1), D(2026, 4, 1)),
    (102, D(2026, 4, 1, 18, 40), D(2026, 4, 1), D(2026, 4, 1)),
    (103, D(2026, 4, 3, 12, 5), D(2026, 4, 3), D(2026, 4, 1)),
    (107, D(2026, 4, 9, 13, 45), D(2026, 4, 9), D(2026, 4, 1)),
]
# 101 and 102 are hours apart (18:40 minus 09:15 is 9h25m)
assert D(2026, 4, 1, 18, 40) - D(2026, 4, 1, 9, 15) == datetime.timedelta(hours=9, minutes=25)
assert q("SELECT count(*) FROM orders WHERE ordered_at = DATE '2026-04-01'") == [(0,)]
assert q("SELECT count(*) FROM orders WHERE date_trunc('day', ordered_at) = DATE '2026-04-01'") == [(2,)]
assert q("SELECT date_trunc('month', TIMESTAMP '2027-03-15 10:00:00')") == [(D(2027, 3, 1),)]
assert q("SELECT date_trunc('month', TIMESTAMP '2026-03-02 10:00:00')") == [(D(2026, 3, 1),)]
assert q("SELECT typeof(date_trunc('month', DATE '2026-04-09'))") == [("TIMESTAMP",)]
assert q("SELECT count(*) FROM orders WHERE date_trunc('month', ordered_at) = DATE '2026-04-01'") == [(7,)]
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT extract(month FROM DATE '2026-03-01'), extract(month FROM DATE '2027-03-01')") == [(3, 3)]
assert q("SELECT count(*) FROM orders WHERE date_trunc('day', ordered_at) = TIMESTAMP '2026-04-01 09:15:00'") == [(0,)]
# source: https://duckdb.org/docs/current/sql/functions/date
# confirmed: date_trunc(part, date) "Truncate to specified precision. Always returns a TIMESTAMP, even when the input is a DATE."
# source: https://www.postgresql.org/docs/current/functions-datetime.html
# confirmed: Postgres documents date_trunc, e.g. date_trunc('hour', timestamp '2001-02-16 20:38:40') gives 2001-02-16 20:00:00

# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model", so Postgres is a server database; the note no longer calls it popular, which no page here supports
