# checks for notes/202-retention-who-came-back-the-month-after.md
import os, sys
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
j = lambda m: date(2026, m, 1)
COH = "cohorts AS (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id)"
ACT = "active AS (SELECT {d} customer_id, CAST(date_trunc('month', login_on) AS DATE) AS active_month FROM logins)"
TAIL = "SELECT c.cohort, count(*) AS customers, count(a.customer_id) AS came_back FROM cohorts AS c {j} JOIN active AS a ON a.customer_id = c.customer_id AND a.active_month = {m} GROUP BY c.cohort ORDER BY c.cohort"
def run(d, j, m):
    return q(f"WITH {COH}, {ACT.format(d=d)} {TAIL.format(j=j, m=m)}")
# per customer story in the table, in python
months = {}
for cid, d in q("SELECT customer_id, login_on FROM logins"):
    months.setdefault(cid, set()).add(d.month)
assert months == {1: {1, 2, 3}, 2: {1}, 3: {2}, 4: {2}, 5: {3}}
back = {c: (min(m) + 1) in m for c, m in months.items()}
assert back == {1: True, 2: False, 3: False, 4: False, 5: False}
# main query: january 2 and 1, february 2 and 0, march 1 and 0
assert run("DISTINCT", "LEFT", "c.cohort + INTERVAL 1 MONTH") == [(j(1), 2, 1), (j(2), 2, 0), (j(3), 1, 0)]
# answer 1: inner join leaves one row, january 1 and 1
assert run("DISTINCT", "INNER", "c.cohort + INTERVAL 1 MONTH") == [(j(1), 1, 1)]
# answer 2: no DISTINCT, cohort month itself, february shows 3 (Chirag logs in twice in february)
assert run("", "LEFT", "c.cohort") == [(j(1), 2, 2), (j(2), 3, 3), (j(3), 1, 1)]
assert q("SELECT count(*) FROM logins WHERE customer_id = 3 AND login_on >= DATE '2026-02-01' AND login_on < DATE '2026-03-01'") == [(2,)]
# the latest logins are in march, so april cannot show a come-back
assert q("SELECT max(login_on) FROM logins") == [(date(2026, 3, 8),)]
# cohort is the first login month, not the signup month: Disha joined in march but first logged in in february
assert q("SELECT month(c.joined_on), min(month(l.login_on)) FROM customers c JOIN logins l USING (customer_id) WHERE c.name = 'Disha' GROUP BY 1") == [(3, 2)]
# CAST turns the timestamp date_trunc returns into a plain date (note 132)
assert q("SELECT typeof(date_trunc('month', DATE '2026-01-05')), typeof(CAST(date_trunc('month', DATE '2026-01-05') AS DATE))") == [("TIMESTAMP", "DATE")]
