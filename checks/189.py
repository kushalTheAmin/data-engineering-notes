# checks for notes/189-running-totals.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import datetime as dt
con = shop()
q = lambda s: con.execute(s).fetchall()
placed = [r[0] for r in q("SELECT placed FROM daily_orders ORDER BY day")]
assert placed == [2, 0, 1, 1, 0, 1, 0, 1, 1]
total, run = 0, []
for p in placed:
    total += p
    run.append(total)
assert run == [2, 2, 3, 4, 4, 5, 5, 6, 7]
assert 2 + 0 + 1 + 1 + 0 + 1 == 5 and run[5] == 5
got = q("SELECT day, placed, sum(placed) OVER (ORDER BY day) AS running FROM daily_orders ORDER BY day")
assert [g[2] for g in got] == run and len(got) == 9
assert got[0][0] == dt.date(2026, 4, 1) and got[5][0] == dt.date(2026, 4, 6)
# OVER () gives 7 on every row
assert {r[0] for r in q("SELECT sum(placed) OVER () FROM daily_orders")} == {7}
assert run[-1] == sum(placed) == 7
# day never repeats
assert q("SELECT count(*), count(DISTINCT day) FROM daily_orders") == [(9, 9)]
# DESC flips it
d = q("SELECT day, running FROM (SELECT day, sum(placed) OVER (ORDER BY day DESC) AS running FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-09') ORDER BY day")
assert d == [(dt.date(2026, 4, 1), 7), (dt.date(2026, 4, 9), 1)]
# cancelled: only april 4 has 1; WHERE first makes april 9 a 0, filter outside gives 1
assert q("SELECT day FROM daily_orders WHERE cancelled = 1") == [(dt.date(2026, 4, 4),)]
assert q("SELECT day, sum(cancelled) OVER (ORDER BY day) AS running FROM daily_orders WHERE day = DATE '2026-04-09'") == [(dt.date(2026, 4, 9), 0)]
assert q("SELECT running FROM (SELECT day, sum(cancelled) OVER (ORDER BY day) AS running FROM daily_orders) AS t WHERE day = DATE '2026-04-09'") == [(1,)]
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: with ORDER BY in OVER the sum runs from the first row up through the current one, and a WHERE-removed row is not seen by any window function
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: the default frame with ORDER BY is all rows from the partition start up through the current row's last ORDER BY peer
# rows that tie in the ORDER BY all show the same running value, which counts all of them
assert q("SELECT x, sum(x) OVER (ORDER BY k) FROM (VALUES (1, 5), (1, 7), (2, 1)) AS t(k, x) ORDER BY x") == [(1, 13), (5, 12), (7, 12)]
assert 5 + 7 == 12 and 5 + 7 + 1 == 13
