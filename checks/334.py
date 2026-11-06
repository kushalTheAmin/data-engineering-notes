# checks for notes/334-errors-in-scripts-catching-them-without-hiding-them.md
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
price = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(price["dhokla"]) == 6.0 and float(price["masala chai"]) == 3.0
items = con.execute("SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE order_id = 101 ORDER BY 1").fetchall()
assert items == [("dhokla", 2), ("masala chai", 2)], items
assert 6.0 * 2 + 3.0 * 2 == 18.0 and 6.0 * 2 == 12.0 and 18.0 - 12.0 == 6.0
assert float(price["khandvi"]) == 7.5 and float(price["fafda"]) == 4.5 and 4.5 * 3 == 13.5
assert 6.0 * 1 + 3.0 * 1 == 9.0
src = ('PRICES = {"dhokla": 6.00, "masala chai": 3.00}\nlines = [("dhokla", 2), ("masalla chai", 2)]\n\n'
       'total = 0\nfor name, qty in lines:\n    total += PRICES[name] * qty\nprint(total)\n')
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "total.py"), "w").write(src)
    r = subprocess.run([sys.executable, "total.py"], cwd=d, capture_output=True, text=True)
    assert r.returncode != 0 and 'total.py", line 6, in <module>' in r.stderr
    assert "total += PRICES[name] * qty" in r.stderr and r.stderr.strip().endswith("KeyError: 'masalla chai'"), r.stderr
try:
    6.0 * "2"
    raise SystemExit("expected TypeError")
except TypeError:
    pass
# source: https://docs.python.org/3/tutorial/errors.html
# confirmed: Exception is a wildcard that catches almost everything; the common pattern is to print or log it and re-raise

# audit: with pass instead of the append the note printed skipped: [] (not just total), so the line vanishes with no record
src2 = ('PRICES = {"dhokla": 6.00, "masala chai": 3.00}\nlines = [("dhokla", 2), ("masalla chai", 2)]\n\n'
        'total = 0\nskipped = []\nfor name, qty in lines:\n    try:\n        total += PRICES[name] * qty\n    except KeyError:\n        pass\n\n'
        'print("total:", total)\nprint("skipped:", skipped)\n')
r = subprocess.run([sys.executable, "-c", src2], capture_output=True, text=True)
assert r.stdout == "total: 12.0\nskipped: []\n", r.stdout
