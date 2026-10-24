# checks for notes/197-generate-series-a-column-of-consecutive-days.md
import os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
d = lambda n: date(2026, 4, n)
# python loop, stop day included by <=
days = []
day = d(1)
while day <= d(9):
    days.append(day)
    day += timedelta(days=1)
assert (len(days), days[0], days[-1]) == (9, d(1), d(9))
assert q("SELECT CAST(d AS DATE) AS day FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS t(d)") == [(x,) for x in days]
# orders: 7 rows, 6 different days
assert q("SELECT count(*), count(DISTINCT CAST(ordered_at AS DATE)) FROM orders") == [(7, 6)]
# zero rows when start is after stop, no error
assert q("SELECT * FROM generate_series(DATE '2026-04-09', DATE '2026-04-01', INTERVAL 1 DAY)") == []
# range leaves the stop out
assert q("SELECT count(*) FROM range(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY)") == [(8,)]
# duckdb gives timestamps back
assert q("SELECT typeof(d) FROM generate_series(DATE '2026-04-01', DATE '2026-04-02', INTERVAL 1 DAY) AS t(d) LIMIT 1") == [("TIMESTAMP",)]
# answer 1: step 2 from april 2 never lands on april 9
assert q("SELECT CAST(d AS DATE) FROM generate_series(DATE '2026-04-02', DATE '2026-04-09', INTERVAL 2 DAY) AS t(d)") == [(d(2),), (d(4),), (d(6),), (d(8),)]
assert [d(2) + timedelta(days=2 * k) for k in range(4)][-1] == d(8) and d(2) + timedelta(days=8) == d(10)
# answer 2: 9 days minus 6 order days = 3 empty days (april 2, 5, 7)
assert q("SELECT count(*) FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS t(d) WHERE CAST(d AS DATE) NOT IN (SELECT CAST(ordered_at AS DATE) FROM orders)") == [(3,)]
assert 9 - 7 == 2
assert q("SELECT CAST(d AS DATE) FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS t(d) WHERE CAST(d AS DATE) NOT IN (SELECT CAST(ordered_at AS DATE) FROM orders)") == [(d(2),), (d(5),), (d(7),)]
assert q("SELECT count(*) FROM orders WHERE CAST(ordered_at AS DATE) = DATE '2026-04-01'") == [(2,)]
# source: https://www.postgresql.org/docs/current/functions-srf.html
# confirmed: "When step is positive, zero rows are returned if start is greater than stop." and Postgres has generate_series
# source: https://duckdb.org/docs/2.0/sql/functions/list.html
# confirmed: "the stop parameter is exclusive" for range and "the stop parameter is inclusive" for generate_series
# source: https://duckdb.org/docs/2.0/sql/functions/utility.html
# confirmed: table functions, "generate_series(start, stop, step) Returns a table of values between start and stop (inclusive)" and "range(start, stop, step) ... (exclusive)"
# source: https://duckdb.org/docs/2.0/sql/functions/timestamp.html
# confirmed: "generate_series(timestamp, timestamp, interval) Generate a table of timestamps in the closed range, stepping by the interval."
# source: https://www.postgresql.org/docs/current/functions-srf.html
# confirmed: Postgres examples write the step as a quoted string, '1 day'::interval, not DuckDB's INTERVAL 1 DAY
