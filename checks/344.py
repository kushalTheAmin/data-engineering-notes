# checks for notes/344-practice-dedupe-and-count-orders-in-plain-python.md
import os, sys, subprocess, re, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "344-practice-dedupe-and-count-orders-in-plain-python.md")).read()
# every python block in the note runs and matches its output block (the gate does it too); here the key numbers
con = shop()
feed = con.execute("SELECT customer_id, city, CAST(changed_at AS VARCHAR) FROM city_feed").fetchall()
assert len(feed) == 5
assert len(set(feed)) == 4  # exact copies dropped
latest = {}
for cid, city, ts in feed:
    if cid not in latest or ts > latest[cid][1]:
        latest[cid] = (city, ts)
assert len(latest) == 3
assert latest == {1: ("Hoboken", "2026-04-12 18:30:00"), 2: ("Edison", "2026-04-10 09:05:00"), 4: ("Hoboken", "2026-04-11 07:45:00")}
first = {}
for cid, city, ts in feed:
    first.setdefault(cid, city)
assert first == {1: "Jersey City", 2: "Edison", 4: "Hoboken"}
cities = {}
for cid, city, ts in feed:
    cities.setdefault(cid, set()).add(city)
assert [c for c in cities if len(cities[c]) > 1] == [1]
assert {c: len(v) for c, v in cities.items()} == {1: 2, 2: 1, 4: 1}
# 2 customers have 2 rows each, so counting rows says 2 moved
rows_per = {}
for cid, _, _ in feed: rows_per[cid] = rows_per.get(cid, 0) + 1
assert sum(1 for v in rows_per.values() if v > 1) == 2
# the JSON in the note holds the real 7 orders
raw = re.search(r"raw = '(\[.*?\])'", src).group(1)
note_orders = json.loads(raw)
db = con.execute("SELECT order_id, status FROM orders ORDER BY 1").fetchall()
assert [(o["order_id"], o["status"]) for o in note_orders] == db
assert len(db) == 7
delivered = sum(1 for _, s in db if s == "delivered")
assert delivered == 5
dup = note_orders + note_orders[:2]
assert len(dup) == 9 and sum(1 for o in dup if o["status"] == "delivered") == 7
# text timestamps in YYYY-MM-DD HH:MM:SS compare in time order
from datetime import datetime
ts = [t for _, _, t in feed]
assert sorted(ts) == sorted(ts, key=lambda s: datetime.fromisoformat(s))
# a dictionary cannot be a dictionary key
try:
    {}[{"a": 1}] = 1
    raise SystemExit("should fail")
except TypeError as e:
    assert str(e) == "unhashable type: 'dict'"
# source: https://docs.python.org/3/glossary.html
# confirmed (opened this run): "mutable containers (such as lists or dictionaries) are not [hashable]"; hashability makes an object usable as a dictionary key; tuples are hashable if their elements are
assert hash(("1", "Jersey City")) is not None
