# checks for notes/042-line-endings.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

lf = b"101,delivered\n102,delivered\n"
crlf = lf.replace(b"\n", b"\r\n")
assert len(lf) == 28 and len(crlf) == 30
assert b"\n".hex() == "0a" and b"\r\n".hex(" ") == "0d 0a"
status = crlf.split(b"\n")[0].split(b",")[1]
assert status == b"delivered\r" and status != b"delivered"

rows = shop().execute("SELECT order_id, status FROM orders ORDER BY order_id").fetchall()
assert len(rows) == 7
lf_size = sum(len(f"{i},{s}") + 1 for i, s in rows)
crlf_size = sum(len(f"{i},{s}") + 2 for i, s in rows)
assert crlf_size - lf_size == 7
# q2: CRLF between lines, no ending after the last
data = "\r\n".join(f"{i},{s}" for i, s in rows).encode()
hits = [l.split(b",")[0] for l in data.split(b"\n") if l.split(b",")[1] == b"delivered"]
assert hits == [b"107"]
assert sum(1 for _, s in rows if s == "delivered") == 5
# source: https://en.wikipedia.org/wiki/Newline
#   confirmed: LF is 0A (\n) on Unix-like systems incl. Linux and macOS; CR LF is 0D 0A (\r\n) on Windows;
#   CR and LF came from teletype/typewriter style printing; files moved between Windows and Unix can be misread
# source: https://docs.python.org/3/library/functions.html
#   confirmed: open() with newline=None (default) turns \n, \r and \r\n into \n when reading
print("042 ok")
