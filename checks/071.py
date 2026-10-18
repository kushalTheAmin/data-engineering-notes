# checks for notes/071-exploding-lists-into-many-rows.md
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
items = con.execute("""SELECT o.order_id, o.customer_id, p.name, i.quantity FROM orders o
  JOIN order_items i USING (order_id) JOIN products p USING (product_id)
  WHERE o.order_id IN (105, 106) ORDER BY o.order_id, i.quantity DESC, p.name""").fetchall()
assert sorted(items) == sorted([(105, 4, "kaju katli", 2), (105, 4, "jalebi", 2), (105, 4, "masala chai", 1), (106, 1, "khandvi", 2)])
records = [
    '{"order_id": 105, "customer_id": 4, "items": [{"product": "kaju katli", "quantity": 2}, {"product": "jalebi", "quantity": 2}, {"product": "masala chai", "quantity": 1}]}',
    '{"order_id": 106, "customer_id": 1, "items": [{"product": "khandvi", "quantity": 2}]}',
]
def explode(texts):
    rows = []
    for text in texts:
        order = json.loads(text)
        for item in order["items"]:
            rows.append({"order_id": order["order_id"], "customer_id": order["customer_id"], **item})
    return rows
rows = explode(records)
assert len(records) == 2 and len(rows) == 4
assert [(r["order_id"], r["customer_id"], r["product"], r["quantity"]) for r in rows] == [(105, 4, "kaju katli", 2), (105, 4, "jalebi", 2), (105, 4, "masala chai", 1), (106, 1, "khandvi", 2)]
assert sum(1 for r in rows if r["order_id"] == 105) == 3
# order_items: 13 rows for 7 orders
assert con.execute("SELECT count(*), count(DISTINCT order_id) FROM order_items").fetchone() == (13, 7)
# check yourself 2: empty list gives no rows
assert explode(['{"order_id": 108, "customer_id": 2, "items": []}']) == []
# source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.explode.html
#   confirmed: "Transform each element of a list-like to a row, replicating index values"; "empty list-likes will result in a np.nan for that row"
print("071 ok")
