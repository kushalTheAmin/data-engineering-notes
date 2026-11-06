# checks for notes/341-reading-json-in-python-the-whole-file-at-once.md
import os, sys, subprocess, json, io
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "341-reading-json-in-python-the-whole-file-at-once.md")).read()
blocks = [b.split("```", 1)[0] for b in src.split("```python\n")[1:]]
outs = ["list 3", "{'order_id': 104, 'customer_id': 3, 'status': 'cancelled'}", "delivered: 2 2"]
r = subprocess.run([sys.executable, "-I", "-c", blocks[0]], capture_output=True, text=True)
assert r.stdout.splitlines() == outs, r.stdout
r = subprocess.run([sys.executable, "-I", "-c", blocks[1]], capture_output=True, text=True)
assert r.stdout.splitlines() == ["Extra data: line 2 column 1 (char 41)", "[105, 106]"], r.stdout
# real shop rows 101, 102, 104, 105, 106
from _shop import shop
rows = shop().execute("SELECT order_id, customer_id, status FROM orders WHERE order_id IN (101,102,104,105,106) ORDER BY 1").fetchall()
assert rows == [(101,1,"delivered"),(102,2,"delivered"),(104,3,"cancelled"),(105,4,"delivered"),(106,1,"pending")], rows
# json.load takes the whole file in one read call
class F(io.StringIO):
    calls = 0
    def read(self, *a):
        F.calls += 1
        return super().read(*a)
assert json.load(F('[{"a": 1}]')) == [{"a": 1}] and F.calls == 1
# numbers stay numbers
assert type(json.loads('{"order_id": 104}')["order_id"]) is int
# two delivered of the three, counted twice
assert 2 == sum(1 for s in ["delivered", "delivered", "cancelled"] if s == "delivered")
# the 41st character is where line 2 starts
first = '{"order_id": 105, "status": "delivered"}\n'
assert len(first) == 41
# source: https://docs.python.org/3/library/json.html
# confirmed (opened this run): json.load(fp) "Deserialize fp to a Python object", fp is a .read()-supporting file
