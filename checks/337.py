# checks for notes/337-functions-as-values-handing-a-function-to-another-function.md
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT name, price FROM products WHERE name IN ('dhokla','kaju katli','masala chai','fafda') ORDER BY product_id").fetchall()
assert [(n, float(p)) for n, p in rows] == [("dhokla", 6.0), ("kaju katli", 12.0), ("masala chai", 3.0), ("fafda", 4.5)], rows
assert [n for n, p in sorted(rows, key=lambda r: r[1])] == ["masala chai", "fafda", "dhokla", "kaju katli"]
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "337-functions-as-values-handing-a-function-to-another-function.md")).read()
code = src.split("```python\n", 1)[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout.split("\n")[1] == "4", r.stdout
# 4 products, key called once each
# source: https://docs.python.org/3/howto/sorting.html
# confirmed: the key function is called exactly once for each input record
assert max(rows, key=lambda r: r[1])[0] == 'kaju katli'
# audit: key can return any comparable value, not only a number; 338 sorts by a name string
assert [p["name"] for p in sorted([{"name": "b"}, {"name": "a"}], key=lambda p: p["name"])] == ["a", "b"]
# audit: the third printed line (the parentheses trap) was never asserted
assert r.stdout.split("\n")[2] == "by_price() missing 1 required positional argument: 'p'", r.stdout
# source: https://docs.python.org/3/library/functions.html
# confirmed (opened this run): sorted "Return a new sorted list from the items in iterable"; max and min say key "specifies a one-argument ordering function like that used for list.sort()"
ps = [{"price": 3}, {"price": 1}]
assert sorted(ps, key=lambda p: p["price"]) is not ps and ps[0]["price"] == 3
assert max(ps, key=lambda p: p["price"]) == {"price": 3} and min(ps, key=lambda p: p["price"]) == {"price": 1}
