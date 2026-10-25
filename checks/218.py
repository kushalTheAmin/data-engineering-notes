# checks for notes/218-key-constraints-primary-key-and-references-in-create-table.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
def refused(sql, word):
    try:
        con.execute(sql)
    except Exception as e:
        return word in str(e).lower()
    return False
# orders 101 and 102 exist, 999 does not
assert q("SELECT order_id FROM orders WHERE order_id IN (101, 102, 999) ORDER BY order_id") == [(101,), (102,)]
# no rules table takes all three inserts
con.execute("CREATE TABLE loose (shipment_id INTEGER, order_id INTEGER, via VARCHAR)")
con.execute("INSERT INTO loose VALUES (1, 101, 'bike'), (1, 102, 'van'), (2, 999, 'van')")
assert q("SELECT * FROM loose") == [(1, 101, "bike"), (1, 102, "van"), (2, 999, "van")]
# keyed table: first insert stored, repeat id and orphan refused
con.execute("CREATE TABLE shipments (shipment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders (order_id), via VARCHAR)")
con.execute("INSERT INTO shipments VALUES (1, 101, 'bike')")
assert refused("INSERT INTO shipments VALUES (1, 102, 'van')", "primary key")
assert refused("INSERT INTO shipments VALUES (2, 999, 'van')", "foreign key")
assert q("SELECT count(*) FROM shipments") == [(1,)]
# check yourself 1
con.execute("CREATE TABLE ship2 (shipment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders (order_id))")
con.execute("INSERT INTO ship2 VALUES (1, 101), (2, 101)")
assert q("SELECT count(*), count(DISTINCT order_id) FROM ship2") == [(2, 1)]
# check yourself 2
con.execute("CREATE TABLE ship3 (shipment_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders (order_id))")
con.execute("INSERT INTO ship3 VALUES (3, NULL)")
assert q("SELECT count(*), count(order_id) FROM ship3") == [(1, 0)]
# source: https://docs.snowflake.com/en/sql-reference/constraints-overview
#   confirmed (opened this run): on standard tables PRIMARY KEY, FOREIGN KEY and UNIQUE are "Optional, not enforced"; NOT NULL and CHECK are enforced.
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): a referencing row need not satisfy the foreign key if any referencing column is null; declare NOT NULL to prevent that.
