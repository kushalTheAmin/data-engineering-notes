# checks for notes/176-scalar-subqueries-one-value-inside-a-query.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
products = [("dhokla", 6.00), ("khandvi", 7.50), ("jalebi", 5.00), ("kaju katli", 12.00), ("masala chai", 3.00), ("fafda", 4.50)]
assert q("SELECT count(*) FROM products") == [(6,)]
avg_price = sum(p for _, p in products) / len(products)
assert avg_price == 6.333333333333333 and round(avg_price, 2) == 6.33
assert [n for n, p in products if p > avg_price] == ["khandvi", "kaju katli"]
assert q("SELECT name, price FROM products WHERE price > (SELECT avg(price) FROM products) ORDER BY price") == [("khandvi", Decimal("7.50")), ("kaju katli", Decimal("12.00"))]
# the sweet inner query has two rows: jalebi and kaju katli
assert q("SELECT name FROM products WHERE category = 'sweet' ORDER BY name") == [("jalebi",), ("kaju katli",)]
try:
    q("SELECT name FROM products WHERE price > (SELECT price FROM products WHERE category = 'sweet')")
    raise SystemExit("should have failed")
except Exception as e:
    assert "More than one row returned by a subquery" in str(e)
# zero rows: the scalar is NULL, no error, empty result
assert q("SELECT (SELECT price FROM products WHERE category = 'frozen')") == [(None,)]
assert q("SELECT name FROM products WHERE price > (SELECT price FROM products WHERE category = 'frozen')") == []
# check yourself 1: 4 below average, 2 above, none equal, 6 total, not 3
assert q("SELECT name FROM products WHERE price < (SELECT avg(price) FROM products) ORDER BY price") == [("masala chai",), ("fafda",), ("jalebi",), ("dhokla",)]
assert 4 + 2 == 6 and q("SELECT count(*) FROM products WHERE price = (SELECT avg(price) FROM products)") == [(0,)]
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed (4.2.11): "A scalar subquery is an ordinary SELECT query in parentheses that returns exactly one row with one column"; "It is an error to use a query that returns more than one row or more than one column"; "if, during a particular execution, the subquery returns no rows, there is no error; the scalar result is taken to be null"
