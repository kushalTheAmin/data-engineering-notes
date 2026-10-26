# checks for notes/224-upsert-insert-or-update-in-one-statement.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE menu (name VARCHAR PRIMARY KEY, price DECIMAL(6, 2))")
con.execute("INSERT INTO menu SELECT name, price FROM products")
assert q("SELECT count(*) FROM menu") == [(6,)]
# a plain insert of jalebi is refused, the name is already there
try:
    con.execute("INSERT INTO menu VALUES ('jalebi', 5.50)")
    raise SystemExit("insert should have failed")
except Exception as e:
    assert "primary key" in str(e).lower()
up = "INSERT INTO menu VALUES ('jalebi', 5.50), ('imarti', 6.00) ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price"
con.execute(up)
rows = q("SELECT name, price FROM menu ORDER BY name")
assert rows == [("dhokla", Decimal("6.00")), ("fafda", Decimal("4.50")), ("imarti", Decimal("6.00")), ("jalebi", Decimal("5.50")), ("kaju katli", Decimal("12.00")), ("khandvi", Decimal("7.50")), ("masala chai", Decimal("3.00"))]
# running it twice gives the same 7 rows
con.execute(up)
assert q("SELECT name, price FROM menu ORDER BY name") == rows
assert len(rows) == 7
# DO NOTHING skips the repeat
con.execute("INSERT INTO menu VALUES ('jalebi', 9.00) ON CONFLICT (name) DO NOTHING")
assert q("SELECT price FROM menu WHERE name = 'jalebi'") == [(Decimal("5.50"),)]
# question 1: dhokla matches, chai is a new key, 6 + 1 = 7
con.execute("CREATE TABLE menu2 (name VARCHAR PRIMARY KEY, price DECIMAL(6, 2))")
con.execute("INSERT INTO menu2 SELECT name, price FROM products")
con.execute("INSERT INTO menu2 VALUES ('dhokla', 6.50), ('chai', 3.00) ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price")
assert q("SELECT count(*) FROM menu2") == [(7,)]
# question 2: no key, the upsert errors
con.execute("CREATE TABLE loose AS SELECT name, price FROM products")
try:
    con.execute(up.replace("menu", "loose"))
    raise SystemExit("upsert should have failed")
except Exception as e:
    assert "conflict target" in str(e)
# source: https://www.postgresql.org/docs/current/sql-insert.html
# confirmed: ON CONFLICT DO UPDATE guarantees an atomic INSERT or UPDATE outcome, even under high concurrency
# source: https://duckdb.org/docs/2.0/sql/statements/insert.html
#   confirmed (opened this run): "DuckDB supports two such clauses: ON CONFLICT DO NOTHING and ON CONFLICT DO UPDATE SET ..."; "the special virtual table EXCLUDED, which contains the conflicting values for the row"; "A conflict target ... is a group of columns that an index or uniqueness/key constraint is defined on"
