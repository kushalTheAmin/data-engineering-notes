# checks for notes/196-gaps-and-islands-one-row-per-streak.md
import os, sys
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
inner = "SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders WHERE placed > 0"
d = lambda n: date(2026, 4, n)
# python: the same grouping with a dict of buckets
days = [d(n) for n in (1, 3, 4, 6, 8, 9)]
buckets = {}
for n, x in enumerate(days, start=1):
    buckets.setdefault(x.toordinal() - n, []).append(x)
streaks = sorted((min(v), max(v), len(v)) for v in buckets.values())
assert streaks == [(d(1), d(1), 1), (d(3), d(4), 2), (d(6), d(6), 1), (d(8), d(9), 2)]
assert len(days) == 6 and len(streaks) == 4
assert q(f"SELECT min(day) AS first_day, max(day) AS last_day, count(*) AS days FROM ({inner}) AS t GROUP BY label ORDER BY first_day") == streaks
# answer 1
assert [(a, (b - a).days, c) for a, b, c in streaks] == [(d(1), 0, 1), (d(3), 1, 2), (d(6), 0, 1), (d(8), 1, 2)]
assert q(f"SELECT min(day) AS first_day, max(day) - min(day) AS span, count(*) AS days FROM ({inner}) AS t GROUP BY label ORDER BY first_day") == [(a, s, c) for a, s, c in [(d(1), 0, 1), (d(3), 1, 2), (d(6), 0, 1), (d(8), 1, 2)]]
# answer 2
assert q(f"SELECT count(*) AS streaks FROM (SELECT day FROM ({inner}) AS t GROUP BY day)") == [(6,)]
# source: https://duckdb.org/docs/stable/sql/query_syntax/groupby
# confirmed earlier: GROUP BY groups rows sharing a value; see note 143 check
