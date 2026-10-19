# checks for notes/079-a-table-rows-are-records-columns-are-fields.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
got = con.execute("SELECT customer_id, name, city, CAST(joined_on AS VARCHAR) FROM customers WHERE customer_id >= 3 ORDER BY customer_id").fetchall()
assert got == [(3, "Chirag", "Jersey City", "2026-02-11"), (4, "Disha", "Hoboken", "2026-03-02"), (5, "Esha", None, "2026-03-15")]
rows = [dict(zip(["customer_id", "name", "city", "joined_on"], r)) for r in got]
assert rows[2] == {"customer_id": 5, "name": "Esha", "city": None, "joined_on": "2026-03-15"}
assert [r["city"] for r in rows] == ["Jersey City", "Hoboken", None]
assert all(r.keys() == rows[0].keys() for r in rows)
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
#   confirmed: a DataFrame is "Two-dimensional, size-mutable, potentially heterogeneous tabular data"
# a database table keeps the same columns in every row, and name cannot hold NULL
import duckdb
try:
    con.execute("INSERT INTO customers VALUES (9, NULL, NULL, DATE '2026-04-01')"); assert False
except duckdb.ConstraintException:
    pass
con.execute("INSERT INTO customers VALUES (9, 'Test', NULL, DATE '2026-04-01')")  # city allows NULL
print("079 ok")
