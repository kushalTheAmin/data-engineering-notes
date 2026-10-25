# checks for notes/200-session-ids-a-running-sum-of-the-flags.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
F = "WITH flagged AS (SELECT customer_id, clicked_at, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (PARTITION BY customer_id ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t) "
# python: running sum of the flags per customer
flags = {1: [1, 0, 0, 1, 0], 2: [1, 1]}
ids = {c: [sum(v[:i + 1]) for i in range(len(v))] for c, v in flags.items()}
assert ids == {1: [1, 1, 1, 2, 2], 2: [1, 2]}
rows = q(F + "SELECT customer_id, new_session, sum(new_session) OVER (PARTITION BY customer_id ORDER BY clicked_at) FROM flagged ORDER BY customer_id, clicked_at")
assert [r[1] for r in rows] == [1, 0, 0, 1, 0, 1, 1]
assert [r[2] for r in rows] == [1, 1, 1, 2, 2, 1, 2]
# (customer_id, session_id) is unique per session: 4 sessions, 2 per customer
assert len({(r[0], r[2]) for r in rows}) == 4
# answer 1: no PARTITION BY, one running sum over all 7 clicks in time order
r1 = q(F + "SELECT customer_id, sum(new_session) OVER (ORDER BY clicked_at) FROM flagged ORDER BY customer_id, clicked_at")
assert [r[1] for r in r1 if r[0] == 2] == [2, 3]
assert [r[1] for r in r1 if r[0] == 1] == [1, 2, 2, 4, 4]
# answer 2: no ORDER BY inside OVER, every Asha row is the total 2
r2 = q(F + "SELECT sum(new_session) OVER (PARTITION BY customer_id) FROM flagged WHERE customer_id = 1")
assert [r[0] for r in r2] == [2] * 5
# a window function cant sit inside another one: duckdb refuses it
try:
    q("SELECT sum(lag(x) OVER (ORDER BY x)) OVER (ORDER BY x) FROM range(3) t(x)")
    assert False
except Exception as e:
    assert "window function calls cannot be nested" in str(e)
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: syntax description says each argument is "any value expression that does not itself contain window function calls", so a window call cannot sit inside another;
#   (the page also says "Window function calls are permitted only in the SELECT list and the ORDER BY clause of the query.")
