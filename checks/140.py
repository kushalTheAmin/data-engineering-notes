# checks for notes/140-sum-and-avg-adding-up-and-averaging.md
import os, sys
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
prices = [float(p[0]) for p in q("SELECT price FROM products ORDER BY product_id")]
assert prices == [6.00, 7.50, 5.00, 12.00, 3.00, 4.50]
total = 0
count = 0
for p in prices:
    total += p
    count += 1
assert (total, count, total / count) == (38.0, 6, 6.333333333333333)
assert q("SELECT sum(price), avg(price), count(*) FROM products") == [(Decimal("38.00"), 6.333333333333333, 6)]
assert q("SELECT sum(price), avg(price), count(*) FROM products WHERE category = 'snack'") == [(Decimal("18.00"), 6.0, 3)]
assert 6.33 not in prices and 6.333333333333333 not in prices
assert q("SELECT price FROM products WHERE name = 'dhokla'") == [(Decimal("6.00"),)]
assert q("SELECT price FROM products WHERE name = 'khandvi'") == [(Decimal("7.50"),)]
assert q("SELECT price FROM products WHERE name = 'kaju katli'") == [(Decimal("12.00"),)]
# price is exact decimal, sum stays decimal, avg is a float in DuckDB
assert q("SELECT typeof(price) FROM products LIMIT 1") == [("DECIMAL(6,2)",)]
assert q("SELECT typeof(sum(price)), typeof(avg(price)) FROM products") == [("DECIMAL(38,2)", "DOUBLE")]
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: avg is "the average (arithmetic mean) of all the non-null input values"
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is "steamed to a cake-like consistency", so a steamed savory cake
assert q("SELECT avg(price) FROM products WHERE category = 'snack'") == [(6.0,)]
assert abs(38 / 6 - 6.333333333333333) < 1e-12 and round(38 / 6, 2) == 6.33
