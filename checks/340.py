# checks for notes/340-reading-a-csv-in-python-row-by-row.md
import os, sys, subprocess, csv, io
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "340-reading-a-csv-in-python-row-by-row.md")).read()
code = src.split("```python\n")[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout.splitlines() == ["{'order_id': '104', 'customer_id': '3', 'ordered_at': '2026-04-04 08:30:00', 'status': 'cancelled'}", "delivered: 2", "second loop: 0"], r.stdout
# real shop rows 101, 102, 104
from _shop import shop
rows = shop().execute("SELECT order_id, customer_id, CAST(ordered_at AS VARCHAR), status FROM orders WHERE order_id IN (101,102,104) ORDER BY 1").fetchall()
assert rows == [(101,1,"2026-04-01 09:15:00","delivered"),(102,2,"2026-04-01 18:40:00","delivered"),(104,3,"2026-04-04 08:30:00","cancelled")], rows
# the reader pulls lines lazily: after reading one row, only 2 lines (header + row) were taken
pulled = []
def lines():
    for l in ["a,b\n", "1,2\n", "3,4\n", "5,6\n"]:
        pulled.append(l); yield l
rd = csv.DictReader(lines())
next(rd)
assert len(pulled) == 2
# a second pass over an exhausted reader is empty
rd = csv.DictReader(io.StringIO("a,b\n1,2\n"))
assert len(list(rd)) == 1 and len(list(rd)) == 0
# every value is text
assert all(isinstance(v, str) for v in next(csv.DictReader(io.StringIO("a\n104\n"))).values())
# source: https://docs.python.org/3/library/csv.html
# confirmed: file objects should be opened with newline=''
# source: https://docs.python.org/3/library/csv.html
# confirmed (opened this run): DictReader "maps the information in each row to a dict whose keys are given by the optional fieldnames parameter"; if fieldnames is omitted, the values in the first row are used as the fieldnames
assert next(csv.DictReader(io.StringIO("a,b\n1,2\n"))) == {"a": "1", "b": "2"}
# audit: with newline='' a line break inside a quoted value stays part of that value
import tempfile
p = os.path.join(tempfile.mkdtemp(), "q.csv")
with open(p, "w", newline="") as f: f.write('a,b\n1,"x\ny"\n')
with open(p, newline="") as f: assert list(csv.DictReader(f)) == [{"a": "1", "b": "x\ny"}]
# source: https://docs.python.org/3/library/csv.html
# confirmed (opened this run): "If newline='' is not specified, newlines embedded inside quoted fields will not be interpreted correctly"
