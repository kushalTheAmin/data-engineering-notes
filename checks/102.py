# checks for notes/102-a-database-in-one-file.md
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
# the two rows shown are real customers rows
assert con.execute("SELECT name, city FROM customers WHERE name IN ('Asha','Bhavin') ORDER BY customer_id").fetchall() == [("Asha", "Jersey City"), ("Bhavin", "Edison")]
# a file database survives close and reopen; an in-memory one does not
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "shop.duckdb")
    c = duckdb.connect(p)
    c.execute("CREATE TABLE customers (name VARCHAR, city VARCHAR)")
    c.execute("INSERT INTO customers VALUES ('Asha', 'Jersey City'), ('Bhavin', 'Edison')")
    c.close()
    assert os.path.exists(p)
    c = duckdb.connect(p)
    assert len(c.execute("SELECT * FROM customers").fetchall()) == 2
    c.close()
m = duckdb.connect(":memory:")
m.execute("CREATE TABLE t (x INTEGER)")
m.close()
assert len(duckdb.connect(":memory:").execute("SELECT * FROM duckdb_tables()").fetchall()) == 0
# source: https://duckdb.org/docs/current/connect/overview.html
# confirmed: in-memory mode (":memory:" or no file) loses all data when the process finishes; a path opens or creates a database file
# source: https://duckdb.org/docs/current/connect/concurrency.html
# confirmed: in read-write mode one process can both read and write the database
# source: https://www.sqlite.org/onefile.html
# confirmed: a database in SQLite is a single disk file
print("102 ok")
