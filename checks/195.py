# checks for notes/195-gaps-and-islands-date-minus-row-number.md
import os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT day, placed FROM daily_orders ORDER BY day")
assert len(rows) == 9
days = [r[0] for r in rows if r[1] > 0]
assert days == [date(2026, 4, d) for d in (1, 3, 4, 6, 8, 9)] and len(days) == 6
# python: the label is date minus counter
labels = [d - timedelta(days=n) for n, d in enumerate(days, start=1)]
assert labels == [date(2026, 3, 31), date(2026, 4, 1), date(2026, 4, 1), date(2026, 4, 2), date(2026, 4, 3), date(2026, 4, 3)]
assert len(set(labels)) == 4
g = "day - CAST(row_number() OVER (ORDER BY day) AS INTEGER)"
assert q(f"SELECT day, {g} AS label FROM daily_orders WHERE placed > 0 ORDER BY day") == list(zip(days, labels))
# answer 1: numbering all 9 days keeps the counter in step with the date
assert q(f"SELECT DISTINCT {g} AS label FROM daily_orders") == [(date(2026, 3, 31),)]
assert all(d - timedelta(days=n) == date(2026, 3, 31) for n, d in enumerate([r[0] for r in rows], start=1))
# answer 2: april 4 listed twice
dup = sorted(days + [date(2026, 4, 4)])
dl = [d - timedelta(days=n) for n, d in enumerate(dup, start=1)]
assert dl == [date(2026, 3, 31), date(2026, 4, 1), date(2026, 4, 1), date(2026, 3, 31), date(2026, 4, 1), date(2026, 4, 2), date(2026, 4, 2)]
assert q(f"SELECT day, {g} AS label FROM (SELECT day FROM daily_orders WHERE placed > 0 UNION ALL SELECT DATE '2026-04-04') AS t ORDER BY day, label") == sorted(zip(dup, dl))
assert dl[4] == dl[1] == dl[2]
# duckdb: row_number is BIGINT, date minus BIGINT has no match, so the cast is needed
try:
    q("SELECT DATE '2026-04-01' - CAST(1 AS BIGINT)")
    raise SystemExit("expected a binder error")
except Exception as e:
    assert "No function matches" in str(e)
assert q("SELECT DATE '2026-04-01' - CAST(1 AS INTEGER)") == [(date(2026, 3, 31),)]
# source: https://www.red-gate.com/simple-talk/sql/t-sql-programming/introduction-to-gaps-and-islands-analysis
# confirmed: gaps and islands finds consecutive sequences (islands) and missing values (gaps) in ordered data
