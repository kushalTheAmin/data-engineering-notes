# checks for notes/225-alter-table-adding-a-column-to-a-table-with-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE menu AS SELECT name, price FROM products WHERE price < 6")
assert q("SELECT name FROM menu ORDER BY name") == [("fafda",), ("jalebi",), ("masala chai",)]
con.execute("ALTER TABLE menu ADD COLUMN vegan BOOLEAN")
rows = q("SELECT * FROM menu ORDER BY name")
assert rows == [("fafda", Decimal("4.50"), None), ("jalebi", Decimal("5.00"), None), ("masala chai", Decimal("3.00"), None)]
con.execute("ALTER TABLE menu ADD COLUMN in_stock BOOLEAN DEFAULT true")
rows = q("SELECT * FROM menu ORDER BY name")
assert all(r[2] is None and r[3] is True for r in rows) and len(rows) == 3
try:
    con.execute("ALTER TABLE menu ADD COLUMN vegan VARCHAR")
    raise SystemExit("should have failed")
except Exception as e:
    assert "already exists" in str(e)
# source: https://www.postgresql.org/docs/current/sql-altertable.html
# confirmed: existing rows get NULL; a non-volatile DEFAULT is stored in metadata so the ALTER is very fast on large tables with no rewrite; a volatile default such as clock_timestamp() rewrites the whole table
