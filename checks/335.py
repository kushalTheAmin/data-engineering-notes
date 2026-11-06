# checks for notes/335-with-opening-and-closing-things-safely.md
import os, sys, subprocess, tempfile, errno
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
orders = dict(con.execute("SELECT order_id, status FROM orders WHERE order_id IN (101, 102)").fetchall())
assert orders == {101: "delivered", 102: "delivered"}, orders
assert len("101,delivered\n") == 14 and len("102,delivered\n") == 14
items = con.execute("SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id) WHERE order_id = 105 ORDER BY i.product_id DESC").fetchall()
assert sorted(items) == [("jalebi", 2), ("kaju katli", 2), ("masala chai", 1)], items
price = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(price["kaju katli"]) == 12.0 and 12.0 * 2 == 24.0 and "jalebi" in price
assert errno.errorcode[errno.EMFILE] == "EMFILE" and os.strerror(errno.EMFILE) == "Too many open files"
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "335-with-opening-and-closing-things-safely.md")).read()
code = src.split("```python\n", 1)[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout == "open, file size: 0\nclosed, file size: 14\nafter the error, closed: True file: 102,delivered\n", r.stdout
# source: https://docs.python.org/3/tutorial/inputoutput.html
# confirmed: with closes the file after its suite finishes even if an exception is raised; write without with or close may not be fully written to disk even if the program exits successfully
# source: https://docs.python.org/3/library/errno.html
# confirmed: errno.EMFILE means Too many open files
# audit: a 9000 byte write is visible before close, so small writes only are held back (buffer 8192 by default; docs: https://docs.python.org/3/library/functions.html#open)

# audit: the note said python only scopes names inside functions, but classes and modules do too; the claim is now that a with block has no scope of its own
with open(os.path.join(tempfile.mkdtemp(), "x"), "w") as _f:
    pass
assert _f.closed
# source: https://docs.python.org/3/reference/executionmodel.html
#   confirmed (opened this run): "The following are blocks: a module, a function body, and a class definition." (with is not listed, so names bound in it belong to the enclosing block)
