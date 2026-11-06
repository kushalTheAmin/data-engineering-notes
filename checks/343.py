# checks for notes/343-calling-an-api-from-python-status-first-then-parse.md
import os, sys, subprocess, socket
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "343-calling-an-api-from-python-status-first-then-parse.md")).read()
code = src.split("```python\n")[1].split("```", 1)[0]
r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
assert r.stdout.splitlines() == [
    "(200, {'order_id': 101, 'customer_id': 1, 'status': 'delivered'})",
    "(401, 'unknown caller')",
    "(404, 'no such order')"], (r.stdout, r.stderr)
# question 1: without the except, a 401 raises HTTPError
pre = code.split("key = os.environ")[0]
r = subprocess.run([sys.executable, "-I", "-c", pre + "\ntry:\n    urllib.request.urlopen(urllib.request.Request(base + '/orders/101', headers={'x-api-key': 'k_report_7f3'}), timeout=5)\nexcept urllib.error.HTTPError as e:\n    print(e.code, str(e))"], capture_output=True, text=True)
assert r.stdout.strip() == "401 HTTP Error 401: Unauthorized", r.stdout
# question 2: order 101 belongs to customer 1, so 1 + 1 = 2, and JSON numbers parse as int
from _shop import shop
assert shop().execute("SELECT customer_id FROM orders WHERE order_id = 101").fetchall() == [(1,)]
import json
assert json.loads('{"customer_id": 1}')["customer_id"] + 1 == 2
# no default timeout in python sockets, so urlopen without timeout waits indefinitely
assert socket.getdefaulttimeout() is None
# source: https://docs.python.org/3/library/urllib.request.html
# confirmed (opened this run): non-200 responses end in HTTPDefaultErrorHandler raising HTTPError; timeout not given uses the global default timeout
# source: https://requests.readthedocs.io/en/latest/api/
# confirmed (opened this run): Response.raise_for_status() "Raises HTTPError, if one occurred", so requests only raises when asked
