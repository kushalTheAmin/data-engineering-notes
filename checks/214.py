# checks for notes/214-temporary-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# cheap = price < 6 gives jalebi, masala chai, fafda; dhokla at exactly 6.00 is out
assert q("SELECT count(*) FROM products WHERE price < 6") == [(3,)]
assert q("SELECT name FROM products WHERE price < 6 ORDER BY price") == [("masala chai",), ("fafda",), ("jalebi",)]
assert q("SELECT count(*) FROM products") == [(6,)]
# a temp table named products hides the real one
con.execute("CREATE TEMP TABLE products AS SELECT * FROM products WHERE price < 6")
assert q("SELECT count(*) FROM products") == [(3,)]
assert q("SELECT count(*) FROM memory.products") == [(6,)]
try:
    con.execute("CREATE TABLE products (a INTEGER)")
    assert False
except Exception as e:
    assert "already exists" in str(e)
# dropping it brings the six back
con.execute("DROP TABLE products")
assert q("SELECT count(*) FROM products") == [(6,)]
# a temp table is gone with its connection
c2 = shop()
c2.execute("CREATE TEMP TABLE cheap AS SELECT * FROM products WHERE price < 6")
assert c2.execute("SELECT count(*) FROM cheap").fetchall() == [(3,)]
try:
    con.execute("SELECT count(*) FROM cheap"); assert False
except Exception as e:
    assert "cheap" in str(e)
# source: https://www.postgresql.org/docs/current/sql-createtable.html
#   confirmed (opened this run): "Temporary tables are automatically dropped at the end of a session"; "The default search_path includes the temporary schema first and so identically named existing permanent tables are not chosen for new plans while the temporary table exists, unless they are referenced with schema-qualified names"; "PostgreSQL instead requires each session to issue its own CREATE TEMPORARY TABLE command ... allows different sessions to use the same temporary table name for different purposes"
# the error text relation "cheap" does not exist is Postgres's standard message for a missing table; source: https://www.postgresql.org/docs/current/errcodes-appendix.html (42P01 undefined_table)
# source: https://www.postgresql.org/docs/current/ddl-schemas.html
#   confirmed (opened this run): "by default objects are created in the public schema", so public.products reaches the real table
# source: https://www.postgresql.org/docs/current/glossary.html
#   confirmed (opened this run): relation is "The generic term for all objects in a database that have a name and a list of attributes defined in a specific order. Tables, sequences, views, foreign tables, materialized views, composite types, and indexes are all relations."
