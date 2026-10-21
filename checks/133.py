# checks for notes/133-casts-that-fail-and-try-cast.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT name, price_text, TRY_CAST(price_text AS DECIMAL(6, 2)) FROM price_export ORDER BY product_id").fetchall()
assert len(rows) == 5
assert [r[2] is None for r in rows] == [False, False, True, True, False]
assert con.execute("SELECT count(*), count(TRY_CAST(price_text AS DECIMAL(6, 2))), avg(TRY_CAST(price_text AS DECIMAL(6, 2))) FROM price_export").fetchone() == (5, 3, 5.5)
assert (6 + 7.5 + 3) / 3 == 5.5
try:
    con.execute("SELECT CAST(price_text AS DECIMAL(6, 2)) FROM price_export")
    raise SystemExit("cast should fail")
except Exception as e:
    assert "Conversion Error" in str(e)
assert [r[0] for r in con.execute("SELECT name FROM price_export WHERE TRY_CAST(price_text AS DECIMAL(6, 2)) > 5 ORDER BY product_id").fetchall()] == ["dhokla", "khandvi"]
assert con.execute("SELECT TRY_CAST('12.5' AS INTEGER), TRY_CAST('twelve' AS INTEGER)").fetchone() == (13, None)
# source: https://duckdb.org/docs/current/sql/data_types/typecasting.html
# confirmed: "TRY_CAST can be used to convert the value into NULL instead of throwing an error"
assert con.execute("SELECT TRY_CAST('99999' AS DECIMAL(6, 2))").fetchone() == (None,)
print("133 ok")
