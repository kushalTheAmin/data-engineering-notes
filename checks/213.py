# checks for notes/213-create-table-naming-a-table-and-its-columns.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE wishlist (customer_id INTEGER, product_id INTEGER, added_on DATE)")
assert q("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'wishlist' ORDER BY ordinal_position") == [
    ("customer_id", "INTEGER"), ("product_id", "INTEGER"), ("added_on", "DATE")]
# a new table has zero rows
assert q("SELECT count(*) FROM wishlist") == [(0,)]
# a second CREATE with the same name errors
try:
    con.execute("CREATE TABLE wishlist (a INTEGER)")
    assert False
except Exception as e:
    assert "already exists" in str(e)
# IF NOT EXISTS on products does nothing and keeps the four original columns
con.execute("CREATE TABLE IF NOT EXISTS products (note VARCHAR)")
assert q("SELECT column_name FROM information_schema.columns WHERE table_name = 'products' ORDER BY ordinal_position") == [
    ("product_id",), ("name",), ("category",), ("price",)]
# source: https://www.postgresql.org/docs/current/sql-createtable.html
#   confirmed (opened this run): "CREATE TABLE will create a new, initially empty table in the current database"; IF NOT EXISTS: "Do not throw an error if a relation with the same name already exists... Note that there is no guarantee that the existing relation is anything like the one that would have been created."
