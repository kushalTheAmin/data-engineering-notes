# checks for notes/345-a-dataframe-a-table-in-memory.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the 4 order slice is real shop rows
got = con.execute("SELECT order_id, customer_id, status FROM orders WHERE order_id IN (101,104,106,107) ORDER BY order_id").fetchall()
assert got == [(101, 1, "delivered"), (104, 3, "cancelled"), (106, 1, "pending"), (107, 2, "delivered")]
assert sum(r[0] for r in got) == 418  # the sum in the note
assert (len(got), len(got[0])) == (4, 3)  # shape: 4 rows, 3 columns
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
# opened this run: DataFrame is "Two-dimensional, size-mutable, potentially heterogeneous tabular data", so columns can differ in type
