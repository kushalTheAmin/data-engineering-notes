# checks for notes/190-window-frames-rows-between.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import datetime as dt
con = shop()
q = lambda s: con.execute(s).fetchall()
placed = [r[0] for r in q("SELECT placed FROM daily_orders ORDER BY day")]
assert placed == [2, 0, 1, 1, 0, 1, 0, 1, 1]
last3 = [sum(placed[max(0, i-2):i+1]) for i in range(len(placed))]
assert last3 == [2, 2, 3, 2, 2, 2, 1, 2, 2]
got = q("SELECT day, placed, sum(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3, sum(placed) OVER (ORDER BY day) AS running FROM daily_orders ORDER BY day")
assert [g[2] for g in got] == last3
assert [g[3] for g in got] == [2, 2, 3, 4, 4, 5, 5, 6, 7]
assert got[5][0] == dt.date(2026, 4, 6) and 1 + 0 + 1 == 2 == last3[5]
# first row sees only itself
assert last3[0] == 2 and placed[0] == 2
# avg over the frame on april 1 divides by 1 row
a = q("SELECT round(avg(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) FROM daily_orders ORDER BY day")
assert a[0] == (2.0,) and round(2 / 3, 2) == 0.67
# answer 1
w = q("SELECT day, s FROM (SELECT day, sum(placed) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS s FROM daily_orders) AS t WHERE day IN (DATE '2026-04-02', DATE '2026-04-06') ORDER BY day")
assert w == [(dt.date(2026, 4, 2), 3), (dt.date(2026, 4, 6), 1)]
assert 2 + 0 + 1 == 3 and 0 + 1 + 0 == 1
# answer 2: april 5 dropped, frame reaches april 3 and 4
d = q("SELECT day, sum(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3 FROM daily_orders WHERE day = DATE '2026-04-06' OR day < DATE '2026-04-05'")
assert d == [(dt.date(2026, 4, 1), 2), (dt.date(2026, 4, 2), 2), (dt.date(2026, 4, 3), 3), (dt.date(2026, 4, 4), 2), (dt.date(2026, 4, 6), 3)]
assert 1 + 1 + 1 == 3
# every day has a row
assert q("SELECT count(*) FROM daily_orders") == [(9,)]
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: "In ROWS mode ... the option means that the frame starts or ends the specified number of rows before or after the current row"; "In ROWS mode, CURRENT ROW simply means the current row"; ROWS BETWEEN is in the frame syntax
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: by default, if ORDER BY is supplied then the frame consists of all rows from the start of the partition up through the current row, so the running column is a frame that starts at the first row
