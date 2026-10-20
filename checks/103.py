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
    assert repr(c.execute("SELECT price FROM products").fetchall()[0][0]) == "Decimal('6.00')"
    assert isinstance(c.execute("SELECT name, price FROM products").fetchall(), list)
    c.close()
    # note 102 saves a customers table in shop.duckdb, so loading the shop into that same file fails; the note uses fullshop.duckdb
    c = duckdb.connect(os.path.join(d, "shop102.duckdb"))
    c.execute("CREATE TABLE customers (name VARCHAR, city VARCHAR)")
    try:
        c.execute(sql)
        raise SystemExit("load into the note 102 file should fail")
    except duckdb.CatalogException:
        pass
    c.close()
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: "a savoury sponge dish" "made with a fermented batter that is steamed to a cake-like consistency"
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: a savory snack of Gujarati cuisine, tightly rolled bite-sized pieces, primarily made of gram flour and yogurt
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: native to Gujarat; "gram flour" dough, flattened and "deep-fried till they turn crispy"
# source: https://en.wikipedia.org/wiki/Gram_flour
# confirmed: "Chickpea flour, common varieties include besan or gram flour."
# source: https://www.postgresql.org/docs/current/app-pgdump.html
# confirmed: pg_dump script dumps are plain-text files of the SQL commands needed to rebuild the database, restored by feeding them to psql
# source: https://docs.python.org/3/tutorial/datastructures.html
# confirmed: tuples are immutable sequences (see Tuples and Sequences)
print("103 ok")
