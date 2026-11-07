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
# the dataframe claims, run for real
import pandas as pd
df = pd.DataFrame([dict(order_id=a, customer_id=b, status=c) for a, b, c in got])
assert df.shape == (4, 3) and int(df["order_id"].sum()) == 418 and list(df.index) == [0, 1, 2, 3]
assert str(df["order_id"].dtype) == "int64"  # a whole number column stays whole numbers
# "usually one type": a column can hold mixed values (dtype object), so one type per column is not a rule
assert pd.DataFrame({"a": [1, "x", 2.5]})["a"].tolist() == [1, "x", 2.5]
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html
# opened this run: shape "Return a tuple representing the dimensionality of the DataFrame", rows and columns counts
# source: https://pandas.pydata.org/docs/getting_started/install.html
# opened this run: pandas can be installed from PyPI with pip install pandas
