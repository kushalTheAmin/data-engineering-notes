# checks for notes/130-nullif-and-dividing-by-zero.md
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT day, placed, cancelled FROM daily_orders ORDER BY day").fetchall()
assert len(rows) == 9
assert sum(1 for r in rows if r[1] == 0) == 3
assert [str(r[0]) for r in rows if r[1] == 0] == ["2026-04-02", "2026-04-05", "2026-04-07"]
# daily_orders matches the orders table
real = con.execute("SELECT CAST(ordered_at AS DATE), count(*), count(*) FILTER (WHERE status = 'cancelled') FROM orders GROUP BY 1 ORDER BY 1").fetchall()
assert [r for r in rows if r[1] > 0] == real
# the slice
sl = con.execute("SELECT day, placed, cancelled, cancelled / placed, cancelled / NULLIF(placed, 0) FROM daily_orders WHERE day BETWEEN DATE '2026-04-03' AND DATE '2026-04-05' ORDER BY day").fetchall()
assert len(sl) == 3
assert sl[0][3:] == (0.0, 0.0) and sl[1][3:] == (1.0, 1.0)
assert math.isnan(sl[2][3]) and sl[2][4] is None
# average
a, b = con.execute("SELECT avg(cancelled / placed), round(avg(cancelled / NULLIF(placed, 0)), 2) FROM daily_orders").fetchone()
assert math.isnan(a) and b == 0.17
days = [r for r in rows if r[1] > 0]
assert len(days) == 6 and sum(r[2] / r[1] for r in days) == 1.0 and round(1 / 6, 2) == 0.17
assert con.execute("SELECT NULLIF(5, 0)").fetchone()[0] == 5
assert con.execute("SELECT NULLIF(0, 0)").fetchone()[0] is None
try:
    1 / 0
    assert False
except ZeroDivisionError:
    pass
# source: https://www.postgresql.org/docs/current/functions-conditional.html
# confirmed: NULLIF(value1, value2) returns a null value if value1 equals value2, otherwise value1; described as the inverse of the COALESCE example
# source: https://www.postgresql.org/docs/current/errcodes-appendix.html
# confirmed: the error codes list includes division_by_zero, so Postgres raises an error on division by zero
# source: https://duckdb.org/docs/current/configuration/overview
# confirmed: ieee_floating_point_ops (default true) "Use IEE754-compliant floating point operations (returning NAN instead of errors/NULL)"
# source: https://docs.python.org/3/library/exceptions.html
# confirmed: ZeroDivisionError is a built-in arithmetic error
print("130 ok")
