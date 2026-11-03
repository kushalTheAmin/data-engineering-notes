# checks for notes/313-json-over-http-the-answer-is-text-until-you-parse-it.md
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# Asha is customer 1: orders 101 delivered, 103 delivered, 106 pending
rows = con.execute("SELECT order_id, status FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall()
assert rows == [(101, "delivered"), (103, "delivered"), (106, "pending")]
body = json.dumps([{"order_id": r[0], "status": r[1]} for r in rows])
assert body == '[{"order_id": 101, "status": "delivered"}, {"order_id": 103, "status": "delivered"}, {"order_id": 106, "status": "pending"}]'
assert body[0] == "[" and isinstance(body, str)
orders = json.loads(body)
assert type(orders) is list and orders[2]["status"] == "pending"
assert [o["order_id"] for o in orders if o["status"] == "delivered"] == [101, 103]
try:
    json.loads("<html>oops</html>")
    raise SystemExit("should fail")
except json.JSONDecodeError:
    pass
# a new field does not break a loop that asks only for names it uses
orders[0]["total"] = 12
assert [o["order_id"] for o in orders] == [101, 103, 106]
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
# confirmed: section 8.3 says the Content-Type header field indicates the media type of the content; the header only labels the body, and the receiver gets whatever bytes were sent (a client may even sniff and override it)
print("313 ok")
