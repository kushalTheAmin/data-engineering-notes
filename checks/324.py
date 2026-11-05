# checks for notes/324-capstone-one-shop-order-fetched-from-an-api-hop-by-hop.md
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the row the API reads for order 101
assert q("SELECT order_id, customer_id, status FROM orders WHERE order_id = 101") == [(101, 1, "delivered")]
# the JSON body shown in the note round trips to that row
body = '{"order_id": 101, "customer_id": 1, "status": "delivered"}'
assert json.loads(body) == {"order_id": 101, "customer_id": 1, "status": "delivered"}
assert isinstance(body, str)
# toy waits from note 323: 3 waits of 0.05 seconds, 200 bytes at 1 MB/s
assert round(3 * 0.05, 2) == 0.15
assert round(200 / 1_000_000, 4) == 0.0002
# check yourself 1: order 104 exists and is cancelled, so a good token gets a 200 with that body
assert q("SELECT order_id, status FROM orders WHERE order_id = 104") == [(104, "cancelled")]
# check yourself 2: json.loads on an html page raises an error
try:
    json.loads("<html>unauthorized</html>")
    raise SystemExit("expected a decode error")
except json.JSONDecodeError:
    pass
# the section ran from note 306 to 323, 18 notes, all linked in builds on
assert len(range(306, 324)) == 18
