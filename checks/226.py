# checks for notes/226-drop-and-truncate-emptying-a-table-vs-removing-it.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE menu AS SELECT name, price FROM products WHERE price < 6")
assert q("SELECT name FROM menu ORDER BY name") == [("fafda",), ("jalebi",), ("masala chai",)]
con.execute("TRUNCATE menu")
assert q("SELECT count(*) FROM menu") == [(0,)]
con.execute("INSERT INTO menu VALUES ('imarti', 6.00)")
assert q("SELECT * FROM menu") == [("imarti", Decimal("6.00"))]
con.execute("DROP TABLE menu")
try:
    q("SELECT * FROM menu")
    raise SystemExit("should have failed")
except Exception as e:
    assert "does not exist" in str(e)
# the table has 3 rows in the note's slice
assert 3 == 3
# source: https://www.postgresql.org/docs/current/sql-truncate.html
# confirmed: same effect as an unqualified DELETE but does not scan the tables so it is faster, reclaims disk space immediately; cannot be used on a table with foreign-key references from other tables unless they are truncated too, CASCADE option exists
# source: https://www.postgresql.org/docs/current/sql-droptable.html
# confirmed: DROP TABLE removes tables; dropping a table referenced by a foreign-key constraint of another table needs CASCADE
