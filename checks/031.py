# checks for notes/031-null.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
rows = con.execute("SELECT customer_id, name, city FROM customers").fetchall()
assert len(rows) == 5 and rows[4] == (5, "Esha", None)
assert con.execute("SELECT count(*), count(city) FROM customers").fetchone() == (5, 4)
assert con.execute("SELECT count(*), count(city) FROM customers WHERE name IN ('Disha', 'Esha')").fetchone() == (2, 1)
# python view: a missing value is None
row = {"customer_id": 5, "name": "Esha", "city": None}
assert row["city"] is None
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
#   confirmed: count(*) computes the number of input rows; count("any") counts rows in which the input value is not null
print("031 ok")
