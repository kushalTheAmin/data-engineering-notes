# checks for notes/103-your-first-query-against-the-shop.md
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop, ROOT
import duckdb
from decimal import Decimal
con = shop()
# the query result shown: six products, name and price
assert con.execute("SELECT name, price FROM products").fetchall() == [
    ("dhokla", Decimal("6.00")), ("khandvi", Decimal("7.50")), ("jalebi", Decimal("5.00")),
    ("kaju katli", Decimal("12.00")), ("masala chai", Decimal("3.00")), ("fafda", Decimal("4.50"))]
# loading the file into a file database works once, a second load errors with the table already existing
with tempfile.TemporaryDirectory() as d:
    c = duckdb.connect(os.path.join(d, "shop.duckdb"))
    sql = open(os.path.join(ROOT, "data", "shop.sql"), encoding="utf-8").read()
    c.execute(sql)
    assert c.execute("SELECT name, price FROM products").fetchall()[0] == ("dhokla", Decimal("6.00"))
    try:
        c.execute(sql)
        raise SystemExit("second load should fail")
    except duckdb.CatalogException as e:
        assert 'Table with name "customers" already exists' in str(e)
    c.close()
# source: https://www.postgresql.org/docs/current/app-pgdump.html
# confirmed: pg_dump script dumps are plain-text files of the SQL commands needed to rebuild the database, restored by feeding them to psql
print("103 ok")
