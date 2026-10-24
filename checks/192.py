# checks for notes/192-lag-and-lead-looking-at-the-row-before.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import datetime as dt
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT day, placed FROM daily_orders ORDER BY day")
placed = [r[1] for r in rows]
assert placed == [2, 0, 1, 1, 0, 1, 0, 1, 1]
# python: lag is the list pushed down one, lead is pushed up one
before = [None] + placed[:-1]
after = placed[1:] + [None]
change = [None] + [placed[i] - placed[i-1] for i in range(1, 9)]
assert before == [None, 2, 0, 1, 1, 0, 1, 0, 1]
assert after == [0, 1, 1, 0, 1, 0, 1, 1, None]
assert change == [None, -2, 1, 0, -1, 1, -1, 1, 0]
got = q("SELECT day, placed, lag(placed) OVER (ORDER BY day) AS before, lead(placed) OVER (ORDER BY day) AS after, placed - lag(placed) OVER (ORDER BY day) AS change FROM daily_orders ORDER BY day")
assert [g[2] for g in got] == before and [g[3] for g in got] == after and [g[4] for g in got] == change
# offset and default
assert q("SELECT lag(placed, 1, 0) OVER (ORDER BY day) FROM daily_orders ORDER BY day")[0][0] == 0
# answer 1: WHERE first, so only april 4 and 6 reach the window
kept = [(d, p) for d, p in rows if d in (dt.date(2026, 4, 4), dt.date(2026, 4, 6))]
assert [p for _, p in kept] == [1, 1]
assert q("SELECT day, lag(placed) OVER (ORDER BY day) AS before FROM daily_orders WHERE day IN (DATE '2026-04-04', DATE '2026-04-06') ORDER BY day") == [(dt.date(2026, 4, 4), None), (dt.date(2026, 4, 6), 1)]
assert placed[4] == 0  # the tempting answer, april 5
# answer 2: distance 2
two = [None, None] + placed[:-2]
assert two[1] is None and two[2] == 2 and placed[1] == 0
assert q("SELECT day, two_back FROM (SELECT day, lag(placed, 2) OVER (ORDER BY day) AS two_back FROM daily_orders) AS t WHERE day IN (DATE '2026-04-02', DATE '2026-04-03') ORDER BY day") == [(dt.date(2026, 4, 2), None), (dt.date(2026, 4, 3), 2)]
# source: https://www.postgresql.org/docs/current/functions-window.html
# confirmed: lag returns the value at the row offset rows before the current row; if there is no such row, returns default; offset defaults to 1 and default to NULL. lead is the same for rows after
