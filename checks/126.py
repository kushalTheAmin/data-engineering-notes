# checks for notes/126-date-parts-pulling-out-the-year-month-and-day.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT order_id, ordered_at FROM orders WHERE order_id IN (101, 103, 105, 107) ORDER BY order_id")
assert [(o, t.year, t.month, t.day) for o, t in rows] == [(101, 2026, 4, 1), (103, 2026, 4, 3), (105, 2026, 4, 6), (107, 2026, 4, 9)]
assert q("SELECT extract(month FROM ordered_at) FROM orders WHERE order_id = 107") == [(4,)]
assert q("SELECT typeof(extract(month FROM DATE '2026-04-01'))") == [("BIGINT",)]
assert q("SELECT name FROM customers WHERE extract(month FROM joined_on) = 3 ORDER BY customer_id") == [("Disha",), ("Esha",)]
assert datetime.date(2026, 3, 2).month == datetime.date(2027, 3, 2).month == 3
assert q("SELECT month(DATE '2026-04-01')") == [(4,)]
assert q("SELECT count(DISTINCT extract(year FROM ordered_at)) FROM orders") == [(1,)]
# source: https://www.postgresql.org/docs/current/functions-datetime.html
# confirmed: EXTRACT(field FROM source) retrieves subfields such as year, month, day from date/time values
# source: https://duckdb.org/docs/current/sql/functions/date
# confirmed: extract(part FROM date) "Get subfield from a date."
# source: https://duckdb.org/docs/current/sql/functions/datepart
# confirmed: month(date) "Month." and year(date) "Year."
