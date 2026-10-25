# checks for notes/215-not-null-and-default-required-columns-and-fallback-values.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE cart (customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL DEFAULT 1)")
con.execute("INSERT INTO cart (customer_id, product_id) VALUES (1, 1)")
con.execute("INSERT INTO cart VALUES (2, 3, 4)")
assert q("SELECT * FROM cart") == [(1, 1, 1), (2, 3, 4)]
# a NULL in a NOT NULL column is refused, and so is a typed NULL where a default exists
for bad in ["INSERT INTO cart (customer_id, product_id) VALUES (NULL, 3)", "INSERT INTO cart VALUES (3, 2, NULL)"]:
    try:
        con.execute(bad)
        assert False
    except Exception as e:
        assert "NOT NULL" in str(e)
assert q("SELECT count(*) FROM cart") == [(2,)]
# the opening puzzle: Esha's city is NULL, every customer has a name
assert q("SELECT name FROM customers WHERE city IS NULL") == [("Asha",)] or q("SELECT name FROM customers WHERE city IS NULL") == [("Esha",)]
assert q("SELECT name FROM customers WHERE city IS NULL") == [("Esha",)]
assert q("SELECT count(*) FROM customers WHERE name IS NULL") == [(0,)]
# check yourself 1
con.execute("CREATE TABLE parcel (parcel_id INTEGER, status VARCHAR DEFAULT 'packed')")
con.execute("INSERT INTO parcel VALUES (1, NULL)")
con.execute("INSERT INTO parcel (parcel_id) VALUES (2)")
assert q("SELECT parcel_id, status FROM parcel ORDER BY parcel_id") == [(1, None), (2, "packed")]
# check yourself 2
con.execute("CREATE TABLE people (name VARCHAR NOT NULL, city VARCHAR NOT NULL DEFAULT 'unknown')")
con.execute("INSERT INTO people (name) VALUES ('Esha')")
assert q("SELECT count(*) FROM people WHERE city IS NULL") == [(0,)]
assert q("SELECT city FROM people") == [("unknown",)]
# source: https://www.postgresql.org/docs/current/ddl-default.html
#   confirmed (opened this run): "When a new row is created and no values are specified for some of the columns, those columns will be filled with their respective default values."
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): "A not-null constraint simply specifies that a column must not assume the null value."
