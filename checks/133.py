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
# source: https://www.postgresql.org/docs/current/bookindex.html
# confirmed: the full index of the Postgres docs has no TRY_CAST entry (it lists COALESCE and date_trunc), so Postgres has no TRY_CAST
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model"
assert con.execute("SELECT TRY_CAST('99999' AS DECIMAL(6, 2))").fetchone() == (None,)
# DECIMAL(6, 2): at most 6 digits in total, 2 after the point (see note 022)
assert con.execute("SELECT TRY_CAST('9999.99' AS DECIMAL(6, 2)), TRY_CAST('12345.67' AS DECIMAL(6, 2))").fetchone()[1] is None
assert con.execute("SELECT TRY_CAST('9999.99' AS DECIMAL(6, 2))").fetchone()[0] is not None
print("133 ok")
