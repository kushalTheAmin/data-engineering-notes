# checks for notes/193-top-n-per-group.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
prods = q("SELECT name, category, price FROM products ORDER BY product_id")
assert len(prods) == 6
# python: group, sort each group by price desc, keep first 2
groups = {}
for name, cat, price in prods:
    groups.setdefault(cat, []).append((name, cat, price))
top2 = []
for cat in sorted(groups):
    top2 += sorted(groups[cat], key=lambda r: -r[2])[:2]
assert [r[0] for r in top2] == ["masala chai", "khandvi", "dhokla", "kaju katli", "jalebi"]
assert len(top2) == 5 and len(groups["drink"]) == 1 and len(groups["snack"]) == 3
assert [r for r in groups["snack"] if r[0] == "fafda"][0][2] == Decimal("4.50")
assert sorted(groups["snack"], key=lambda r: -r[2])[2][0] == "fafda"  # 3rd of the snacks, cut
# the real query
assert q("SELECT name, category, price FROM (SELECT name, category, price, row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products) AS t WHERE rn <= 2 ORDER BY category, price DESC") == [(r[0], r[1], r[2]) for r in top2]
# rn <= 1 gives the priciest per category
assert [r[0] for r in q("SELECT name FROM (SELECT name, row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products) AS t WHERE rn = 1 ORDER BY name")] == sorted(max(g, key=lambda r: r[2])[0] for g in groups.values())
# the WHERE version errors
try:
    q("SELECT name FROM products WHERE row_number() OVER (PARTITION BY category ORDER BY price DESC) <= 2")
    assert False
except Exception as e:
    assert "window" in str(e).lower()
# answer 1: no partition, top 2 overall
overall = sorted(prods, key=lambda r: -r[2])[:2]
assert [(r[0], r[2]) for r in overall] == [("kaju katli", Decimal("12.00")), ("khandvi", Decimal("7.50"))]
assert q("SELECT name, price FROM (SELECT name, price, row_number() OVER (ORDER BY price DESC) AS rn FROM products) AS t WHERE rn <= 2 ORDER BY price DESC") == [(r[0], r[2]) for r in overall]
# answer 2: cheapest per category
cheap = sorted(min(g, key=lambda r: r[2])[0] for g in groups.values())
assert cheap == ["fafda", "jalebi", "masala chai"]
assert q("SELECT name FROM (SELECT name, row_number() OVER (PARTITION BY category ORDER BY price) AS rn FROM products) AS t WHERE rn = 1 ORDER BY name") == [(n,) for n in cheap]
assert Decimal("4.50") < Decimal("6.00") < Decimal("7.50")
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: window functions run after WHERE (rows removed by WHERE are not seen by a window function), so a window function result cannot be filtered in the same query level; row_number and PARTITION BY are standard Postgres
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: window function calls are only permitted in the SELECT list and ORDER BY clause of the query
# the prices and categories the prose lists
assert {r[0]: (r[1], r[2]) for r in prods} == {"dhokla": ("snack", Decimal("6.00")), "khandvi": ("snack", Decimal("7.50")), "fafda": ("snack", Decimal("4.50")), "jalebi": ("sweet", Decimal("5.00")), "kaju katli": ("sweet", Decimal("12.00")), "masala chai": ("drink", Decimal("3.00"))}
assert len(groups) == 3
# source: https://www.postgresql.org/docs/current/tutorial-window.html
# confirmed: "the row_number window function assigns sequential numbers to the rows within each partition, in the order defined by the ORDER BY clause (with tied rows numbered in an unspecified order)"; its top-N example adds empno as a second sort column
