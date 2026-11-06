# checks for notes/336-classes-in-one-picture-data-and-functions-together.md
import os, sys, subprocess, tempfile, io
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
items = con.execute("SELECT i.product_id, p.name, p.price, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE order_id IN (105, 106) ORDER BY i.order_id, i.product_id").fetchall()
assert [(n, float(pr), q) for _, n, pr, q in items] == [("jalebi", 5.0, 2), ("kaju katli", 12.0, 2), ("masala chai", 3.0, 1), ("khandvi", 7.5, 2)], items
assert dict(con.execute("SELECT order_id, status FROM orders WHERE order_id IN (105, 106)").fetchall()) == {105: "delivered", 106: "pending"}
assert 12.0 * 2 + 5.0 * 2 + 3.0 * 1 == 37.0 and 7.5 * 2 == 15.0
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "336-classes-in-one-picture-data-and-functions-together.md")).read()
code = src.split("```python\n", 1)[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout == "delivered 37.0\npending 15.0\n37.0\n", r.stdout
class Order:
    def total():
        pass
try:
    Order().total()
    raise SystemExit("no error")
except TypeError as e:
    assert "takes 0 positional arguments but 1 was given" in str(e), e
f = open(os.path.join(tempfile.mkdtemp(), "x"), "w")
assert isinstance(f, io.TextIOWrapper) and callable(f.write) and callable(f.close)
f.close()
