# checks for notes/177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
products = [("dhokla", "snack", 6.00), ("khandvi", "snack", 7.50), ("jalebi", "sweet", 5.00), ("kaju katli", "sweet", 12.00), ("masala chai", "drink", 3.00), ("fafda", "snack", 4.50)]
assert q("SELECT name, category, price FROM products ORDER BY product_id") == [(n, c, Decimal(str(p)).quantize(Decimal("0.01"))) for n, c, p in products]
assert len(products) == 6
# the loop inside a loop, and the trace table
avg_of = {}
for n, c, p in products:
    same = [p2 for _, c2, p2 in products if c2 == c]
    avg_of[n] = sum(same) / len(same)
assert avg_of == {"dhokla": 6.0, "khandvi": 6.0, "jalebi": 8.5, "kaju katli": 8.5, "masala chai": 3.0, "fafda": 6.0}
assert [n for n, c, p in products if p < avg_of[n]] == ["jalebi", "fafda"]
assert q("SELECT name, price FROM products p WHERE price < (SELECT avg(price) FROM products WHERE category = p.category) ORDER BY price") == [("fafda", Decimal("4.50")), ("jalebi", Decimal("5.00"))]
# the shop wide version returns 4, this one 2
assert len(q("SELECT name FROM products WHERE price < (SELECT avg(price) FROM products)")) == 4
# check yourself 1: >= keeps ties and everything above, 4 rows, fafda out
r = q("SELECT name, price FROM products p WHERE price >= (SELECT avg(price) FROM products WHERE category = p.category) ORDER BY price")
assert r == [("masala chai", Decimal("3.00")), ("dhokla", Decimal("6.00")), ("khandvi", Decimal("7.50")), ("kaju katli", Decimal("12.00"))]
assert "fafda" not in [x[0] for x in r] and len(r) == 4
# check yourself 2: category = category is the inner table twice, so the shop wide average
r2 = q("SELECT name, price FROM products p WHERE price < (SELECT avg(price) FROM products WHERE category = category) ORDER BY price")
assert [x[0] for x in r2] == ["masala chai", "fafda", "jalebi", "dhokla"]
assert round(sum(p for _, _, p in products) / 6, 2) == 6.33
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed (4.2.11): "The subquery can refer to variables from the surrounding query, which will act as constants during any one evaluation of the subquery"
# source: https://www.postgresql.org/docs/current/planner-optimizer.html
# confirmed: "executed in a wide variety of different ways, each of which will produce the same set of results" and "the query optimizer will examine each of these possible execution plans, ultimately selecting the execution plan that is expected to run the fastest"
