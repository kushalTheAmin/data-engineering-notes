# checks for notes/349-merging-dataframes-joins-again.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import pandas as pd
con = shop()
c = con.execute("SELECT customer_id, name FROM customers ORDER BY customer_id").fetchall()
o = con.execute("SELECT order_id, customer_id FROM orders ORDER BY order_id").fetchall()
assert len(c) == 5 and len(o) == 7
cust = pd.DataFrame([{"customer_id": a, "name": b} for a, b in c])
orders = pd.DataFrame([{"order_id": a, "customer_id": b} for a, b in o])
inner = cust.merge(orders, on="customer_id")
left = cust.merge(orders, on="customer_id", how="left")
assert (len(inner), len(left)) == (7, 8)
# same counts as sql notes 156 and 159
assert con.execute("SELECT count(*) FROM customers c JOIN orders o ON c.customer_id=o.customer_id").fetchone()[0] == 7
assert con.execute("SELECT count(*) FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id").fetchone()[0] == 8
assert str(inner["order_id"].dtype) == "int64" and str(left["order_id"].dtype) == "float64"
assert list(left["order_id"].tail(3)[:2]) == [104.0, 105.0] and pd.isna(left["order_id"].iloc[7]) and left["name"].iloc[7] == "Esha"
# q1
oi = con.execute("SELECT order_id, product_id, quantity FROM order_items WHERE order_id IN (104,105) ORDER BY order_id, product_id DESC").fetchall()
assert oi == [(104, 1, 3), (105, 5, 1), (105, 4, 2), (105, 3, 2)] or sorted(oi) == [(104, 1, 3), (105, 3, 2), (105, 4, 2), (105, 5, 1)]
orders2 = pd.DataFrame([{"order_id": 104}, {"order_id": 105}, {"order_id": 106}])
items = pd.DataFrame([
    {"order_id": 104, "product_id": 1, "quantity": 3},
    {"order_id": 105, "product_id": 4, "quantity": 2},
    {"order_id": 105, "product_id": 3, "quantity": 2},
    {"order_id": 105, "product_id": 5, "quantity": 1},
])
a = orders2.merge(items, on="order_id"); b = orders2.merge(items, on="order_id", how="left")
assert (len(a), len(b)) == (4, 5) and 1 + 3 == 4
assert str(b["quantity"].tolist()) == "[3.0, 2.0, 2.0, 1.0, nan]"
assert con.execute("SELECT count(*) FROM order_items WHERE order_id IN (104,105)").fetchone()[0] == 4
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 106").fetchone()[0] == 1  # 106 has items in shop; this slice leaves them out on purpose
# q2
x = orders.merge(cust, on="customer_id", how="left")
assert len(x) == 7 and str(x["order_id"].dtype) == "int64"
# fan out claim: orders joined to items is 13 rows, 7 orders (note 164)
assert con.execute("SELECT count(*), count(DISTINCT o.order_id) FROM orders o JOIN order_items i ON o.order_id=i.order_id").fetchone() == (13, 7)
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
# confirmed: how default 'inner', left keeps keys from left frame like a SQL left outer join
# source: https://pandas.pydata.org/docs/user_guide/missing_data.html
# confirmed: an int64 series reindexed with a gap gets NaN and becomes float64
# audit: a missing value only appears when a row goes unmatched, which an outer merge also does, so the note says here only the left merge has one
_o = pd.DataFrame({"customer_id": [1, 2, 3]}).merge(pd.DataFrame({"order_id": [1, 2], "customer_id": [1, 9]}), how="outer", on="customer_id")
assert str(_o["order_id"].dtype) == "float64"
