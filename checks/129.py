# checks for notes/129-the-difference-between-two-dates.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
D = datetime.datetime
a = q("SELECT ordered_at FROM orders WHERE order_id = 102")[0][0]
b = q("SELECT ordered_at FROM orders WHERE order_id = 103")[0][0]
assert a == D(2026, 4, 1, 18, 40) and b == D(2026, 4, 3, 12, 5)
gap = b - a
assert gap == datetime.timedelta(days=1, hours=17, minutes=25)
assert q("SELECT date_diff('day', TIMESTAMP '2026-04-01 18:40:00', TIMESTAMP '2026-04-03 12:05:00')") == [(2,)]
# midnights crossed: april 2 and april 3 start inside the window
assert (b.date() - a.date()).days == 2
assert q("SELECT DATE '2026-04-03' - DATE '2026-04-01'") == [(2,)]
assert q("SELECT date_diff('month', DATE '2026-01-31', DATE '2026-02-01')") == [(1,)]
# source: https://duckdb.org/docs/current/sql/functions/date
# confirmed: date_diff(part, startdate, enddate) is "the number of part boundaries between startdate and enddate"
# source: https://www.postgresql.org/docs/current/functions-datetime.html
# confirmed: date '2001-10-01' - date '2001-09-28' gives 3 (days elapsed)
# date_diff day vs elapsed time disagree on "within 2 days" only when the delivery is dated 2 days after the order and its clock time is later than the order clock time
for gap in range(0, 6):
    for ph in range(24):
        for dh in range(24):
            p, v = datetime.datetime(2026, 4, 1, ph), datetime.datetime(2026, 4, 1 + gap, dh)
            elapsed_ok = v - p <= datetime.timedelta(days=2)
            diff_ok = (v.date() - p.date()).days <= 2
            assert (elapsed_ok != diff_ok) == (gap == 2 and dh > ph)
