# checks for notes/069-json-lines.md
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, status FROM orders WHERE order_id IN (105,106,107) ORDER BY 1").fetchall()
assert rows == [(105, 4, "delivered"), (106, 1, "pending"), (107, 2, "delivered")]
array = '[{"order_id": 105, "status": "delivered"}, {"order_id": 106, "status": "pending"}, {"order_id": 107, "status": "deliv'
lines = '{"order_id": 105, "status": "delivered"}\n{"order_id": 106, "status": "pending"}\n{"order_id": 107, "status": "deliv'
try:
    json.loads(array)
    raise SystemExit("should fail")
except json.JSONDecodeError:
    pass
good = []
for line in lines.split("\n"):
    try:
        good.append(json.loads(line)["order_id"])
    except json.JSONDecodeError:
        pass
assert good == [105, 106]
assert con.execute("SELECT count(*) FROM orders").fetchone()[0] == 7
cols = con.execute("SELECT count(*) FROM information_schema.columns WHERE table_name = 'orders'").fetchone()[0]
assert cols == 4
o = {"order_id": 101, "customer_id": 1, "ordered_at": "2026-04-01 09:15:00", "status": "delivered"}
per = json.dumps(o, indent=2).count("\n") + 1
assert per == 6 and 7 * per == 42
assert "\n" not in json.dumps({"message": "less sweet\nno onion"})
assert json.dumps({"message": "a\nb"}) == '{"message": "a\\nb"}'
assert con.execute("SELECT message FROM order_messages WHERE order_id = 107").fetchone()[0] == "call first\nleave at the door"
assert "\n" not in json.dumps({"message": "call first\nleave at the door"})
half1, half2 = '{"order_id": 107, "message": "call first', 'leave at the door"}'
for piece in (half1, half2):
    try:
        json.loads(piece)
        raise SystemExit("half should fail")
    except json.JSONDecodeError:
        pass
# source: https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json
#   confirmed: "JSON data must be newline-delimited, or ndJSON. Each JSON object must be on a separate line in the file."
print("069 ok")
