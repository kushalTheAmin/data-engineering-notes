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
# audit: timeout is per blocking operation, not a total limit (a server sending 1 byte a second for 6 seconds beat timeout=2)
import threading, time, urllib.request as _ur
_s = socket.socket(); _s.bind(("127.0.0.1", 0)); _s.listen(1)
def _srv():
    c, _ = _s.accept(); c.recv(4096); c.sendall(b"HTTP/1.0 200 OK\r\n\r\n")
    for _ in range(4): time.sleep(1); c.sendall(b"x")
    c.close()
threading.Thread(target=_srv, daemon=True).start()
_t = time.time()
assert len(_ur.urlopen("http://127.0.0.1:%d/" % _s.getsockname()[1], timeout=2).read()) == 4 and time.time() - _t > 3
# source: https://docs.python.org/3/library/urllib.request.html
# confirmed (opened this run): timeout "specifies a timeout in seconds for blocking operations like the connection attempt"
# source: https://requests.readthedocs.io/en/latest/user/quickstart/
# confirmed (opened this run): "In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception. Response.raise_for_status() will raise an HTTPError..."
