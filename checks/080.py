# checks for notes/080-every-column-holds-one-type.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
got = con.execute("SELECT typeof(customer_id), typeof(name), city, typeof(city), typeof(joined_on) FROM customers WHERE customer_id = 5").fetchall()
assert got == [("INTEGER", "VARCHAR", None, "VARCHAR", "DATE")]
try:
    con.execute("INSERT INTO products VALUES (7, 'ladoo', 'sweet', 'free')")
    raise SystemExit("should have failed")
except Exception as e:
    assert "Could not convert" in str(e)
assert con.execute("SELECT count(*) FROM products").fetchone()[0] == 6
# source: https://www.sqlite.org/datatype3.html
#   confirmed: "the datatype of a value is associated with the value itself, not with its container"
print("080 ok")
