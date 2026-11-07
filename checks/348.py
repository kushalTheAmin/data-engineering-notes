# checks for notes/348-groupby-in-pandas-next-to-group-by.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import pandas as pd
con = shop()
got = con.execute("""SELECT o.order_id, o.customer_id, o.status, sum(i.quantity)
FROM orders o JOIN order_items i USING (order_id) WHERE o.order_id IN (101,104,106,107)
GROUP BY ALL ORDER BY o.order_id""").fetchall()
assert got == [(101, 1, "delivered", 4), (104, 3, "cancelled", 3), (106, 1, "pending", 2), (107, 2, "delivered", 2)]  # real rows, items = summed quantity
df = pd.DataFrame([dict(zip(("order_id", "customer_id", "status", "items"), (r[0], r[1], r[2], int(r[3])))) for r in got])
a = df.groupby("customer_id")["items"].agg(["count", "sum"])
assert a.to_dict("index") == {1: {"count": 2, "sum": 6}, 2: {"count": 1, "sum": 2}, 3: {"count": 1, "sum": 3}}
assert 4 + 2 == 6
b = df.groupby("customer_id", as_index=False)["items"].sum()
assert list(b.columns) == ["customer_id", "items"] and list(b["items"]) == [6, 2, 3]
assert list(a.index.names) == ["customer_id"]  # group values became the labels
# customers: Esha has a NULL city, 5 customers
c = con.execute("SELECT name, city FROM customers ORDER BY customer_id").fetchall()
assert len(c) == 5 and c[4] == ("Esha", None)
cust = pd.DataFrame([{"name": n, "city": ci} for n, ci in c])
assert cust.groupby("city")["name"].count().sum() == 4
assert cust.groupby("city", dropna=False)["name"].count().sum() == 5
# sql keeps the NULL group (note 143 shows it)
assert con.execute("SELECT count(*) FROM (SELECT city FROM customers GROUP BY city)").fetchone()[0] == 4
# q1
g1 = df.groupby("status")["items"].sum()
assert g1.to_dict() == {"cancelled": 3, "delivered": 6, "pending": 2}
assert list(g1.items()) == [("cancelled", 3), ("delivered", 6), ("pending", 2)]
assert 4 + 2 == 6  # orders 101 and 107... 101 has 4, 107 has 2
assert list(df["status"])[0] == "delivered"  # appears first, yet sorted output leads with cancelled
# q2
r = con.execute("SELECT order_id, stars FROM order_ratings ORDER BY order_id").fetchall()
assert r == [(101, 5), (102, 4), (103, None), (105, 3), (107, None)]
rd = pd.DataFrame({"order_id": [x[0] for x in r], "stars": [x[1] for x in r]})
g = rd.groupby("stars")["order_id"].count()
assert (len(g), int(g.sum())) == (3, 3)
assert len(rd.groupby("stars", dropna=False)["order_id"].count()) == 4 and len(r) == 5
assert sum(1 for x in r if x[1] is None) == 2
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
# opened this run: dropna default True drops NA group keys, False treats NA as a key; sort default True sorts group keys; as_index=False is "SQL-style" grouped output
# the note's literal customer rows match the shop
assert c == [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
