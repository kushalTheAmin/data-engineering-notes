# checks for notes/149-median-the-middle-value-after-sorting.md
import os, sys
from decimal import Decimal as Dec
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
prices = sorted([6.00, 7.50, 5.00, 12.00, 3.00, 4.50])
assert prices == [3.0, 4.5, 5.0, 6.0, 7.5, 12.0]
mid = len(prices) // 2
assert mid == 3 and (prices[mid - 1] + prices[mid]) / 2 == 5.5
assert prices[len(prices) // 2] == 6.0
assert q("SELECT count(*) FROM products") == [(6,)]
assert q("SELECT round(avg(price), 2) FROM products") == [(6.33,)]
assert q("SELECT count(*) FROM products WHERE price < (SELECT avg(price) FROM products)") == [(4,)]
assert q("SELECT median(price) FROM products") == [(Dec("5.50"),)]
assert q("SELECT category, median(price) FROM products GROUP BY category ORDER BY category") == [("drink", Dec("3.00")), ("snack", Dec("6.00")), ("sweet", Dec("8.50"))]
assert q("SELECT category, count(*) FROM products GROUP BY category ORDER BY category") == [("drink", 1), ("snack", 3), ("sweet", 2)]
assert q("SELECT name FROM products WHERE category = 'snack' AND price = 6.00") == [("dhokla",)]
assert q("SELECT price FROM products WHERE category = 'sweet' ORDER BY price") == [(Dec("5.00"),), (Dec("12.00"),)]
assert q("SELECT count(*) FROM products WHERE price = 8.50") == [(0,)]
# kaju katli at 120.00: average jumps, median stays
r = q("SELECT median(price), avg(price) FROM (SELECT 120.00 AS price UNION ALL SELECT price FROM products WHERE name <> 'kaju katli')")
assert r[0][0] == Dec("5.50") and round(r[0][1], 2) == 24.33
assert q("SELECT name FROM products WHERE price = 12.00") == [("kaju katli",)]
# check yourself
assert q("SELECT median(stars), median(stars_zero_filled) FROM order_ratings") == [(4.0, 3.0)]
assert sorted([5, 4, 3]) == [3, 4, 5] and sorted([0, 0, 3, 4, 5])[2] == 3
# source: https://duckdb.org/docs/2.0/sql/functions/aggregates.html
# confirmed: median(x) is "the middle value of the set. For even value counts, quantitative values are averaged"; also lists quantile_cont(x, 0.5) as its formula
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: percentile_cont(fraction) WITHIN GROUP (ORDER BY ...) "computes the continuous percentile, a value corresponding to the specified fraction within the ordered set"
# source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/MEDIAN.html
# confirmed: "MEDIAN is an inverse distribution function that assumes a continuous distribution model", so the one-word median is not DuckDB only; the Postgres aggregate page lists no median function, only percentile_cont
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model", so Postgres is a server database
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is "a savoury sponge dish" made with a fermented batter "steamed to a cake-like consistency"
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: "Kaju katli (lit. 'Cashew slice') is an Indian dessert." and "Kaju means cashew"
