# checks for notes/325-modules-and-imports-using-code-from-other-files.md
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
price = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(price["dhokla"]) == 6.0 and float(price["masala chai"]) == 3.0
items = con.execute("SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE order_id = 101 ORDER BY p.name").fetchall()
assert items == [("dhokla", 2), ("masala chai", 2)]
assert 6.00 * 2 + 3.00 * 2 == 18.0
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "shop_utils.py"), "w").write(
        'print("loading shop_utils")\nPRICES = {"dhokla": 6.00, "masala chai": 3.00}\ndef line_total(name, qty):\n    return PRICES[name] * qty\n')
    open(os.path.join(d, "report.py"), "w").write(
        'import shop_utils\nimport shop_utils\nprint(shop_utils.line_total("dhokla", 2) + shop_utils.line_total("masala chai", 2))\n')
    out = subprocess.run([sys.executable, "report.py"], cwd=d, capture_output=True, text=True).stdout
    assert out == "loading shop_utils\n18.0\n", out
    open(os.path.join(d, "json.py"), "w").write("print('mine')\n")
    open(os.path.join(d, "t.py"), "w").write("import json\n")
    out = subprocess.run([sys.executable, "t.py"], cwd=d, capture_output=True, text=True).stdout
    assert out == "mine\n", out
# source: https://docs.python.org/3/tutorial/modules.html
#   confirmed (opened this run): each module is only imported once per interpreter session; the scripts directory is first on the search path, ahead of the standard library, so a same-named file is loaded instead
# audit: the note said python looks in the scripts folder before the standard library, a term no earlier note explains. it now says the modules that come with python
