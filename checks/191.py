# checks for notes/191-the-default-frame-trap.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import datetime as dt
con = shop()
q = lambda s: con.execute(s).fetchall()
canc = [r[0] for r in q("SELECT cancelled FROM daily_orders ORDER BY day")]
assert canc == [0, 0, 0, 1, 0, 0, 0, 0, 0]
# python: running max and whole max
run = [max(canc[:i+1]) for i in range(len(canc))]
assert run == [0, 0, 0, 1, 1, 1, 1, 1, 1]
whole = [max(canc)] * len(canc)
assert whole == [1] * 9
got = q("SELECT day, cancelled, max(cancelled) OVER () AS all_max, max(cancelled) OVER (ORDER BY day) AS with_order, max(cancelled) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS whole FROM daily_orders ORDER BY day")
assert [g[2] for g in got] == whole and [g[3] for g in got] == run and [g[4] for g in got] == whole
assert got[3][0] == dt.date(2026, 4, 4)
# last_value: april 5 placed is 0, april 9 placed is 1
placed = [r[0] for r in q("SELECT placed FROM daily_orders ORDER BY day")]
assert placed[4] == 0 and placed[-1] == 1
# answer 1: running min
m = [min(placed[:i+1]) for i in range(len(placed))]
assert m[0] == 2 and m[-1] == 0 and min(placed) == 0
assert q("SELECT day, s FROM (SELECT day, min(placed) OVER (ORDER BY day) AS s FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-09') ORDER BY day") == [(dt.date(2026, 4, 1), 2), (dt.date(2026, 4, 9), 0)]
# answer 2: last_value in default frame is the row itself
assert q("SELECT day, v FROM (SELECT day, last_value(placed) OVER (ORDER BY day) AS v FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-05') ORDER BY day") == [(dt.date(2026, 4, 1), 2), (dt.date(2026, 4, 5), 0)]
assert placed[0] == 2 and placed[4] == 0
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: "The default framing option is RANGE UNBOUNDED PRECEDING ... With ORDER BY, this sets the frame to be all rows from the partition start up through the current row's last ORDER BY peer. Without ORDER BY, ... all rows of the partition"
# source: https://www.postgresql.org/docs/current/functions-window.html
# confirmed: last_value "Returns value evaluated at the row that is the last row of the window frame"
