# checks for notes/339-decorators-the-at-shorthand-for-wrapping-a-function.md
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "339-decorators-the-at-shorthand-for-wrapping-a-function.md")).read()
blocks = src.split("```python\n")
code = blocks[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout.split("\n")[:3] == ["['fafda', 'jalebi', 'dhokla', 'khandvi']", "['dhokla', 'khandvi', 'jalebi', 'fafda']", "wrapper"], r.stdout
# @ is plain assignment
def logged(fn):
    def wrapper(p): return fn(p)
    return wrapper
def f(p): return 1
g = logged(f)
@logged
def f2(p): return 1
assert g.__name__ == f2.__name__ == "wrapper"
# check yourself 1: decorator runs at def time
r = subprocess.run([sys.executable, "-I", "-c", blocks[2].split("```", 1)[0]], capture_output=True, text=True)
assert r.stdout == "decorating by_name\ndefined\n", r.stdout
# check yourself 2: 3 + 3 key calls
r = subprocess.run([sys.executable, "-I", "-c", blocks[3].split("```", 1)[0]], capture_output=True, text=True)
assert r.stdout == "6\n", r.stdout
# real shop rows
from _shop import shop
rows = shop().execute("SELECT name, price FROM products WHERE name IN ('dhokla','khandvi','jalebi','fafda')").fetchall()
ns = {}
exec(code, ns)
assert sorted((n, float(p)) for n, p in rows) == sorted((p["name"], p["price"]) for p in ns["products"])
# source: https://docs.python.org/3/library/functools.html
# confirmed: functools.wraps keeps the decorated function's __name__; without it the name would be 'wrapper'
# source: https://docs.python.org/3/reference/compound_stmts.html
# confirmed: decorator result is bound to the function name instead of the function object
# audit: a decorator need not return a new function; whatever it returns is bound to the name
def reg(fn): return fn
@reg
def f3(p): return 1
assert f3.__name__ == "f3"
# source: https://docs.python.org/3/reference/compound_stmts.html
# confirmed (opened this run): "The result must be a callable, which is invoked with the function object as the only argument. The returned value is bound to the function name instead of the function object."
