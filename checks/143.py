# checks for notes/143-group-by-one-group-per-value.md
import os, sys
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM products") == [(6,)]
assert q("SELECT category, count(*), avg(price) FROM products GROUP BY category ORDER BY category") == [("drink", 1, 3.0), ("snack", 3, 6.0), ("sweet", 2, 8.5)]
assert q("SELECT count(DISTINCT category) FROM products") == [(3,)]
assert q("SELECT city, count(*) FROM customers GROUP BY city ORDER BY city") == [("Edison", 1), ("Hoboken", 1), ("Jersey City", 2), (None, 1)]
assert q("SELECT name FROM customers WHERE city IS NULL") == [("Esha",)]
assert q("SELECT category, count(*) FROM products WHERE price > 5 GROUP BY category ORDER BY category") == [("snack", 2), ("sweet", 1)]
assert q("SELECT stars, count(*), count(stars) FROM order_ratings GROUP BY stars ORDER BY stars") == [(3, 1, 1), (4, 1, 1), (5, 1, 1), (None, 2, 0)]
# python loop shape
products = [("dhokla", "snack", 6.00), ("khandvi", "snack", 7.50), ("jalebi", "sweet", 5.00),
            ("kaju katli", "sweet", 12.00), ("masala chai", "drink", 3.00), ("fafda", "snack", 4.50)]
assert q("SELECT name, category, price FROM products ORDER BY product_id") == [(n, c, Decimal(str(p)).quantize(Decimal("0.01"))) for n, c, p in products]
groups = {}
for name, category, price in products:
    groups.setdefault(category, []).append(price)
assert {k: (len(v), sum(v) / len(v)) for k, v in groups.items()} == {"snack": (3, 6.0), "sweet": (2, 8.5), "drink": (1, 3.0)}

# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "GROUP BY will condense into a single row all selected rows that share the same values for the grouped expressions"; "WHERE filters individual rows before the application of GROUP BY"
# source: https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql
# confirmed: "SQL removes rows that don't meet the conditions in the WHERE clause before it performs any grouping operation"; "The GROUP BY clause doesn't order the result set"; "treats all NULL values as equal and collects them into a single group"
