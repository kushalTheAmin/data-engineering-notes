# checks for notes/201-cohorts-the-month-each-customer-first-showed-up.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT customer_id, login_on FROM logins ORDER BY customer_id, login_on")
assert len(rows) == 8
assert len({r[0] for r in rows}) == 5
# python: earliest login per customer, then its month
first = {}
for c, d in rows:
    first[c] = min(first.get(c, d), d)
cohort = {c: (d.year, d.month) for c, d in first.items()}
assert cohort == {1: (2026, 1), 2: (2026, 1), 3: (2026, 2), 4: (2026, 2), 5: (2026, 3)}
assert [first[c].day for c in (1, 2, 3, 4, 5)] == [5, 20, 3, 14, 8]
by_month = {}
for m in cohort.values():
    by_month[m] = by_month.get(m, 0) + 1
assert by_month == {(2026, 1): 2, (2026, 2): 2, (2026, 3): 1}
# table in the note: login days per customer
days = {c: [(d.month, d.day) for cc, d in rows if cc == c] for c in range(1, 6)}
assert days == {1: [(1, 5), (2, 10), (3, 2)], 2: [(1, 20)], 3: [(2, 3), (2, 25)], 4: [(2, 14)], 5: [(3, 8)]}
# trap: truncating every login counts a customer once per month they logged in
per_month = {}
for c in range(1, 6):
    for m in {m for m, _ in days[c]}:
        per_month[m] = per_month.get(m, 0) + 1
assert per_month == {1: 2, 2: 3, 3: 2}
assert sum(per_month.values()) == 7
# counting login rows per month instead of customers gives 2, 4, 2, so the note says count the customers
assert q("SELECT count(*) FROM logins GROUP BY date_trunc('month', login_on) ORDER BY date_trunc('month', login_on)") == [(2,), (4,), (2,)]
assert q("SELECT count(DISTINCT customer_id) FROM logins GROUP BY date_trunc('month', login_on) ORDER BY date_trunc('month', login_on)") == [(2,), (3,), (2,)]
# answer 2: max puts each customer in their last month
last = {}
for c, d in rows:
    last[c] = max(last.get(c, d), d)
mx = {}
for d in last.values():
    mx[d.month] = mx.get(d.month, 0) + 1
assert mx == {1: 1, 2: 2, 3: 2}
# the sql agrees
r = q("SELECT count(*) FROM (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id) AS t")
assert r[0][0] == 5
# date_trunc hands back a timestamp, which is why the query casts it to a plain date (note 132 explains CAST)
assert q("SELECT typeof(date_trunc('month', DATE '2026-01-05'))") == [("TIMESTAMP",)]
assert q("SELECT typeof(CAST(date_trunc('month', DATE '2026-01-05') AS DATE))") == [("DATE",)]
# source: https://duckdb.org/docs/2.0/sql/functions/date.html
#   confirmed: date_trunc(part, date) "Always returns a TIMESTAMP, even when the input is a DATE", which is why the query casts it back to a date
