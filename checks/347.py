# checks for notes/347-select-columns-and-sort-in-pandas-next-to-select-and-order-by.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import pandas as pd
con = shop()
got = con.execute("SELECT order_id, customer_id, status FROM orders WHERE order_id IN (101,104,106,107) ORDER BY order_id").fetchall()
assert got == [(101, 1, "delivered"), (104, 3, "cancelled"), (106, 1, "pending"), (107, 2, "delivered")]  # real shop rows
df = pd.DataFrame([dict(zip(("order_id", "customer_id", "status"), r)) for r in got])
assert type(df["status"]).__name__ == "Series" and type(df[["status"]]).__name__ == "DataFrame"
assert list(df[["order_id", "status"]].columns) == ["order_id", "status"]
out = df.sort_values(["customer_id", "order_id"], ascending=[True, False])
assert list(out["order_id"]) == [106, 101, 107, 104]
assert list(out.index) == [2, 0, 3, 1]  # labels travel with rows
assert list(df["order_id"]) == [101, 104, 106, 107]  # original untouched
assert len(df) == 4 and len(got) == 4
# customer 1 has two orders (tie), order_id descending puts 106 before 101
assert sorted([r for r in got if r[1] == 1], key=lambda r: -r[0])[0][0] == 106
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
# opened this run: returns a new DataFrame (None only if inplace=True); ascending is "bool or list of bool", a list for multiple sort orders must match the length of by
# source: https://pandas.pydata.org/docs/reference/api/pandas.Series.html
# opened this run: "One-dimensional ndarray with axis labels"
