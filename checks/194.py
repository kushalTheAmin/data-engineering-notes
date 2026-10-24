# checks for notes/194-removing-duplicates-with-row-number.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
feed = q("SELECT customer_id, city, changed_at FROM city_feed")
assert len(feed) == 5
ids = [r[0] for r in feed]
assert sorted(set(ids)) == [1, 2, 4] and ids.count(1) == 2 and ids.count(2) == 2
# python: DISTINCT keeps a row once only if the whole row repeats
seen = []
for r in feed:
    if r not in seen:
        seen.append(r)
assert len(seen) == 4 and sum(1 for r in seen if r[0] == 1) == 2
assert len(q("SELECT DISTINCT customer_id, city, changed_at FROM city_feed")) == 4
# python: newest row per customer
newest = {}
for r in sorted(feed, key=lambda r: r[2]):
    newest[r[0]] = r
keep = [newest[k] for k in sorted(newest)]
assert [(r[0], r[1]) for r in keep] == [(1, "Hoboken"), (2, "Edison"), (4, "Hoboken")]
assert q("SELECT customer_id, city, changed_at FROM (SELECT customer_id, city, changed_at, row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) AS rn FROM city_feed) AS t WHERE rn = 1 ORDER BY customer_id") == keep
assert len(keep) == 3
# Bhavin's two rows are identical
bh = [r for r in feed if r[0] == 2]
assert bh[0] == bh[1]
# answer 2: the dropped rows
dropped = q("SELECT customer_id, city FROM (SELECT customer_id, city, row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) AS rn FROM city_feed) AS t WHERE rn > 1 ORDER BY customer_id")
assert dropped == [(1, "Jersey City"), (2, "Edison")]
assert len(keep) + len(dropped) == len(feed)
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "If SELECT DISTINCT is specified, all duplicate rows are removed from the result set (one row is kept from each group of duplicates)", so rows that differ in any column all stay
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: "the row_number window function assigns sequential numbers to the rows within each partition, in the order defined by the ORDER BY clause (with tied rows numbered in an unspecified order)", so which of two tied rows is number 1 is not promised
# source: https://www.postgresql.org/docs/current/functions-window.html
# confirmed: row_number is a window function; ordering within the window is set by ORDER BY inside OVER
