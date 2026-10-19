# checks for notes/078-capstone-the-shop-orders-three-ways.md
import csv, io, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT customer_id, ordered_at::VARCHAR, status FROM orders WHERE order_id = 103").fetchall() == [(1, "2026-04-03 12:05:00", "delivered")]
assert con.execute("SELECT name FROM customers WHERE customer_id = 1").fetchall() == [("Asha",)]
assert con.execute("SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 103 ORDER BY p.product_id").fetchall() == [("khandvi", 1), ("masala chai", 1)]
csv_text = "order_id,customer,product,quantity\n103,Asha,khandvi,1\n103,Asha,masala chai,1\n"
json_text = '{"order_id": 103, "customer": "Asha", "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]}'
rows = list(csv.DictReader(io.StringIO(csv_text)))
order = json.loads(json_text)
assert len(rows) == 2
assert sum(int(r["quantity"]) for r in rows) == 2 == sum(i["quantity"] for i in order["items"])
assert rows[0]["quantity"] == "1" and order["items"][0]["quantity"] == 1
assert [r[0] for r in con.execute('SELECT count(*) FROM order_items WHERE order_id IN (105,106,107) GROUP BY order_id ORDER BY order_id').fetchall()] == [3, 1, 2]
# check yourself 1: 6 items across orders 105 to 107, 3 orders
assert con.execute("SELECT count(*) FROM order_items WHERE order_id IN (105, 106, 107)").fetchone()[0] == 6
assert con.execute("SELECT count(DISTINCT order_id) FROM order_items WHERE order_id IN (105, 106, 107)").fetchone()[0] == 3
# check yourself 2: json.dumps keeps each message on one line, csv with quotes does not
msgs = con.execute("SELECT order_id, message FROM order_messages ORDER BY 1").fetchall()
assert len(msgs) == 3
text = "".join(json.dumps({"order_id": o, "message": m}) + "\n" for o, m in msgs)
assert text.count("\n") == 3
assert "\\n" in json.dumps({"m": msgs[2][1]})
buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerows(msgs)
assert buf.getvalue().count("\n") == 4
# JSON text cant hold a raw line break inside a value
# source: https://www.rfc-editor.org/rfc/rfc8259
#   confirmed: section 7 says the characters that must be escaped in a string are "quotation mark, reverse solidus, and the control characters (U+0000 through U+001F)"
try:
    json.loads('"a\nb"'); assert False
except json.JSONDecodeError:
    pass
assert json.loads(json.dumps("a\nb")) == "a\nb"
print("078 ok")
