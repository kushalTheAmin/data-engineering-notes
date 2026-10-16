# checks for notes/022-exact-decimal-types.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
# main query: 020 test both ways
rows = con.execute("SELECT name, price, price::DOUBLE + 0.1 + 0.2 = price::DOUBLE + 0.3 AS d, price + 0.1 + 0.2 = price + 0.3 AS x FROM products").fetchall()
assert sum(r[2] for r in rows) == 4 and sum(r[3] for r in rows) == 6 and len(rows) == 6
# price is DECIMAL(6, 2), stored as integer 600 for 6.00
assert con.execute("SELECT typeof(price) FROM products LIMIT 1").fetchone()[0] == "DECIMAL(6,2)"
# DECIMAL(6, 2): 4 digits before the point, top 9999.99, 12345.67 has 5 before
assert 6 - 2 == 4 and len("12345") == 5 and 10 ** 4 - 1 == 9999
try:
    con.execute("SELECT 12345.67::DECIMAL(6, 2)")
    raise SystemExit("should have errored")
except Exception as e:
    assert "Could not cast" in str(e) or "Conversion" in str(e)
assert str(con.execute("SELECT 9999.99::DECIMAL(6, 2)").fetchone()[0]) == "9999.99"
# DECIMAL(8, 2) fits 12345.67
assert str(con.execute("SELECT 12345.67::DECIMAL(8, 2)").fetchone()[0]) == "12345.67"
# scale grows on multiply
assert str(con.execute("SELECT price * 0.15 FROM products WHERE name = 'khandvi'").fetchone()[0]) == "1.1250"
assert 750 * 15 / 100 == 112.5
# rounding back to 2 places
r = dict(con.execute("SELECT name, (price * 0.15)::DECIMAL(6, 2) FROM products WHERE name IN ('khandvi', 'fafda')").fetchall())
assert str(r["khandvi"]) == "1.13" and str(r["fafda"]) == "0.68"
assert 7.50 * 15 // 100 == 1.0 and 112 == 750 * 15 // 100  # chop in cents gives 1.12
assert 450 * 15 // 100 == 67  # fafda chopped is 0.67
# source: https://duckdb.org/docs/current/sql/data_types/numeric.html
#   confirmed: DECIMAL(width, scale) stored as integers sized by width; add, subtract, multiply are exact
# source: https://www.postgresql.org/docs/current/datatype-numeric.html
#   confirmed: numeric is exact, recommended for money, slower than integer or float types, too many digits before the point errors
print("022 ok")
