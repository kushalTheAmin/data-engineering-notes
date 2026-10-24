# checks for notes/199-session-starts-flag-the-click-after-a-long-gap.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
INNER = "SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER ({p} ORDER BY clicked_at), clicked_at) AS gap FROM clicks"
OUT = "SELECT customer_id, clicked_at, gap, CASE WHEN gap IS NULL OR gap > {n} THEN 1 ELSE 0 END AS new_session FROM ({i}) AS t {w} ORDER BY customer_id, clicked_at"
def run(n, p="PARTITION BY customer_id", w=""):
    return q(OUT.format(n=n, i=INNER.format(p=p), w=w))
# the table: 7 clicks, 5 for Asha (1) and 2 for Bhavin (2)
assert q("SELECT customer_id, count(*) FROM clicks GROUP BY customer_id ORDER BY 1") == [(1, 5), (2, 2)]
# python: same gaps with a loop over each customers clicks
from collections import defaultdict
by = defaultdict(list)
for c, t, _ in q("SELECT customer_id, clicked_at, page FROM clicks ORDER BY clicked_at"):
    by[c].append(t)
gaps = {c: [None] + [int((b - a).total_seconds() // 60) for a, b in zip(v, v[1:])] for c, v in by.items()}
assert gaps == {1: [None, 5, 5, 110, 12], 2: [None, 48]}
rows = run(30)
assert [r[2] for r in rows] == [None, 5, 5, 110, 12, None, 48]
flags = [r[3] for r in rows]
assert flags == [1, 0, 0, 1, 0, 1, 1]
# Asha 2 sessions, Bhavin 2 sessions
assert sum(f for r, f in zip(rows, flags) if r[0] == 1) == 2
assert sum(f for r, f in zip(rows, flags) if r[0] == 2) == 2
# NULL > 30 is not true, so the IS NULL test matters
assert q("SELECT CASE WHEN NULL > 30 THEN 1 ELSE 0 END") == [(0,)]
# answer 1: gap > 60 flags 3, Bhavin 09:50 flips to 0
rows60 = run(60)
assert sum(r[3] for r in rows60) == 3 and rows60[-1][3] == 0 and 48 < 60
# answer 2: no PARTITION BY, Bhavin sees ashas clicks: gaps 2 and 40
r2 = run(30, p="", w="WHERE customer_id = 2")
assert [(r[2], r[3]) for r in r2] == [(2, 0), (40, 1)]
# source: https://support.google.com/analytics/answer/9191807
# confirmed: "By default, a session ends or times out after 30 minutes of user inactivity."
# date_diff counts minute boundaries crossed (note 129 shows the same for days), exact here because every click is on a whole minute
assert q("SELECT date_diff('minute', TIMESTAMP '2026-04-01 09:00:59', TIMESTAMP '2026-04-01 09:01:01')") == [(1,)]
assert all(t.second == 0 for (t,) in q("SELECT clicked_at FROM clicks"))
# tempting answer for 1 is 1: only the 110 gap is over 60 once the NULL first clicks are forgotten
assert sum(1 for r in rows60 if r[2] is not None and r[2] > 60) == 1
