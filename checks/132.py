# checks for notes/132-cast-changing-a-values-type.md
import os, sys
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
assert [int(Decimal(x)) for x in ("6.00", "7.50", "4.50")] == [6, 7, 4]
rows = con.execute("SELECT name, price, CAST(price AS INTEGER), CAST(price AS VARCHAR) FROM products WHERE product_id IN (1, 2, 6) ORDER BY product_id").fetchall()
assert [(r[0], r[2], r[3]) for r in rows] == [("dhokla", 6, "6.00"), ("khandvi", 8, "7.50"), ("fafda", 5, "4.50")]
assert con.execute("SELECT '9' < '10', CAST('9' AS INTEGER) < CAST('10' AS INTEGER)").fetchone() == (False, True)
assert "9" > "10" and 9 < 10
# 3 products in the slice
assert len(rows) == 3
# source: https://duckdb.org/docs/current/sql/data_types/typecasting.html
# confirmed: explicit casts use CAST, casting a decimal to an integer rounds ("The number will be rounded"), anything can be cast to VARCHAR
print("132 ok")
