# checks for notes/338-returning-a-function-building-a-function-inside-a-function.md
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "338-returning-a-function-building-a-function-inside-a-function.md")).read()
code = src.split("```python\n", 1)[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout.split("\n")[2] == "6.0 dhokla", r.stdout
ns = {}
exec(code, ns)
assert ns["by_price"] is not ns["by_name"]
assert ns["by_price"].__closure__[0].cell_contents == "price"
assert ns["by_name"].__closure__[0].cell_contents == "name"
# 4 products slice, all real rows
from _shop import shop
rows = shop().execute("SELECT name, price FROM products WHERE name IN ('dhokla','khandvi','jalebi','fafda')").fetchall()
assert sorted((n, float(p)) for n, p in rows) == sorted((p["name"], p["price"]) for p in ns["products"])
# late binding gotcha
fs = [lambda: i for i in range(3)]
assert [f() for f in fs] == [2, 2, 2]
# audit: the 2, 2, 2 needs range(3); a loop over [1, 2, 3] gives 3, 3, 3
fs = []
for i in range(3): fs.append(lambda: i)
assert [f() for f in fs] == [2, 2, 2]
fs = []
for i in [1, 2, 3]: fs.append(lambda: i)
assert [f() for f in fs] == [3, 3, 3]
