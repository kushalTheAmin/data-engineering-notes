# checks for notes/207-capstone-each-customers-first-order-and-the-days-between-orders.md
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
d = dt.date
# python: the same thing with plain loops
orders = q("SELECT c.name, CAST(o.ordered_at AS DATE), o.order_id, o.status FROM customers c JOIN orders o ON c.customer_id = o.customer_id ORDER BY 1, 2")
assert len(orders) == 7
def trace(rows):
    out, prev, seen = [], {}, {}
    for name, day, oid, _ in rows:
        seen[name] = seen.get(name, 0) + 1
        out.append((name, oid, day, seen[name], (day - prev[name]).days if name in prev else None))
        prev[name] = day
    return out
exp = trace(orders)
assert exp == [("Asha", 101, d(2026,4,1), 1, None), ("Asha", 103, d(2026,4,3), 2, 2), ("Asha", 106, d(2026,4,8), 3, 5),
               ("Bhavin", 102, d(2026,4,1), 1, None), ("Bhavin", 107, d(2026,4,9), 2, 8),
               ("Chirag", 104, d(2026,4,4), 1, None), ("Disha", 105, d(2026,4,6), 1, None)]
cte = "WITH o AS (SELECT c.name, CAST(o.ordered_at AS DATE) AS day, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id%s) "
main = "SELECT name, order_id, day, row_number() OVER (PARTITION BY name ORDER BY day) AS nth, day - lag(day) OVER (PARTITION BY name ORDER BY day) AS days_since FROM o ORDER BY name, day"
assert q(cte % "" + main) == exp
# esha has no orders so no row; 4 customers show up
assert len({r[0] for r in exp}) == 4 and q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
# question 1: delivered only
exp1 = trace([r for r in orders if r[3] == 'delivered'])
assert q(cte % " WHERE o.status = 'delivered'" + main) == exp1
assert [r for r in exp1 if r[0] == 'Asha'][-1] == ("Asha", 103, d(2026,4,3), 2, 2)
assert "Chirag" not in {r[0] for r in exp1}
assert (d(2026,4,8) - d(2026,4,3)).days == 5  # the tempting answer
# question 2: avg skips the NULL
gaps = [r[4] for r in exp if r[0] == 'Asha']
assert gaps == [None, 2, 5]
real = [g for g in gaps if g is not None]
assert sum(real) / len(real) == 3.5
assert round(sum(real) / 3, 2) == 2.33  # the tempting answer, NULL counted as 0 and divided by 3
assert q("WITH o AS (SELECT c.name, CAST(o.ordered_at AS DATE) AS day FROM customers c JOIN orders o ON c.customer_id = o.customer_id), g AS (SELECT name, day - lag(day) OVER (PARTITION BY name ORDER BY day) AS days_since FROM o) SELECT name, avg(days_since) AS avg_gap FROM g WHERE name = 'Asha' GROUP BY name") == [("Asha", 3.5)]
# asha ordered on april 1, 3 and 8
assert [r[2] for r in exp if r[0] == 'Asha'] == [d(2026,4,1), d(2026,4,3), d(2026,4,8)]
# source: https://www.postgresql.org/docs/current/tutorial-window.html
#   confirmed (opened this run): "a row removed because it does not meet the WHERE condition is not seen by any window function"
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
#   confirmed (opened this run): avg "Computes the average (arithmetic mean) of all the non-null input values."
